import random

import tweepy
from celery import shared_task
from django.conf import settings

from .models import PredictionLabel
from .models import Search
from .models import Searcher
from .models import Tweet


auth = tweepy.OAuthHandler(
    settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET
)
auth.set_access_token(
    settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
)
TWITTER_API = tweepy.API(auth, wait_on_rate_limit=True)


@shared_task
def collect_tweets(search_id, search_term, number_of_tweets):
    query = f'{search_term} -filter:retweets'
    cursor = tweepy.Cursor(
        TWITTER_API.search, q=query, tweet_mode='extended',
        result_type='recent', include_entities=False
    )

    tweets = []
    for tweet in cursor.items(number_of_tweets):
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
    """This is a dummy classifier task"""

    search = Search.objects.get(pk=search_id)
    labels = PredictionLabel.objects.filter(predictor=search.predictor)

    classified = [(id, date, random.choice(labels)) for id, date, _ in tweets] # noqa

    # TODO: Run these queries within a transaction
    for id, date, label in classified:
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
