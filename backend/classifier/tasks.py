from celery import shared_task

from .collectors import OfficialAPICollector
from .models import Search
from .models import Searcher
from .models import Tweet
from .utils import get_predictor


api_collector = OfficialAPICollector()


@shared_task
def collect_tweets(search_id, search_term, number_of_tweets):
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
    """This is a dummy notifier task"""

    searchers = Searcher.objects.filter(search=search_id)

    for searcher in searchers:
        pass  # Notify via email about clasification results
