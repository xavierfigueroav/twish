"""
This module contains Celery tasks to run heavy routines asynchronously.

Task list:
    * collect_tweets - It collects tweets asynchronously.
    * classify_tweets - It classifies tweets asynchronously.
    * notify_searchers - It notifies registered users after classification
    completes.
"""
from celery import shared_task

from .collectors import OfficialAPICollector
from .models import Search
from .models import Searcher
from .models import Tweet
from .utils import get_predictor


api_collector = OfficialAPICollector()


@shared_task
def collect_tweets(search_id, search_term, number_of_tweets):
    """
    Celery task to collect tweets asynchronously.

    Parameters
    ----------
    search_id : int
        Primary key of the Search instance created for the user search.
    search_term : str
        The user input entered in the application search box.
    number_of_tweets : int
        The number of tweets to collect.
    """

    tweets = []
    for tweet in api_collector.collect(search_term, number_of_tweets):
        tweets.append((tweet.id_str, tweet.created_at, tweet.full_text))
    if len(tweets) == 0:
        search = Search.objects.get(pk=search_id)
        search.empty = True
        search.save()
        notify_searchers.delay(search_id)
    else:
        classify_tweets.delay(search_id, tweets)


@shared_task
def classify_tweets(search_id, tweets):
    """
    Celery task to classify tweets asynchronously. It is called after
    collect_tweets finds tweets.

    Parameters
    ----------
    search_id : int
        Primary key of the Search instance created for the user search.
    tweets : list of triples
        Collection of triples containing tweet information in the following
        order: tweet id, tweet date, tweet text.
    """

    search = Search.objects.get(pk=search_id)
    predictor = get_predictor(predictor=search.predictor)
    prediction = predictor.predict(tweets)

    # TODO: Run these queries within a transaction
    for id, date, label in prediction:
        tweet = Tweet.objects.create(id=id, date=date)  # noqa. What if it already exists?
        search.tweets.add(tweet)  # What if the relationship already exists?
        tweet.predictors.add(
            search.predictor, through_defaults={'label': label}
        )  # What if the relationship already exists?

    notify_searchers.delay(search_id)


@shared_task
def notify_searchers(search_id):
    """
    Celery task to notify registered users after classification completes. It
    is called after classify_tweets ends successfully.

    Parameters
    ----------
    search_id : int
        Primary key of the Search instance created for the user search.
    """

    searchers = Searcher.objects.filter(search=search_id)

    for searcher in searchers:
        pass  # Notify via email about clasification results
