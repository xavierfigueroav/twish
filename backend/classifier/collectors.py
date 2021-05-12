import tweepy
from django.conf import settings


class OfficialAPICollector:
    def __init__(self):
        auth = tweepy.OAuthHandler(
            settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET
        )
        auth.set_access_token(
            settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def collect(self, search_term, number_of_tweets):
        query = f'{search_term} -filter:retweets'
        cursor = tweepy.Cursor(
            self.api.search, q=query, tweet_mode='extended',
            result_type='recent', include_entities=False
        )
        return cursor.items(number_of_tweets)
