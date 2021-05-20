"""
This module contains the classes that encapsulate the business logics to
collect tweets.

The collectors available are:
    * OfficialAPICollector - It collects tweets through the official
    Twitter API.

Notes
-----
It is wanted to add web scraping collectors to bypass the official API
limitations. Feel free to open a pull request.
"""
import tweepy
from django.conf import settings


class OfficialAPICollector:
    """
    This class encapsulates the business logic to collect tweets through the
    official Twitter API.

    Attributes
    ----------
    api : tweepy.API
        Connected and authenticated Tweepy interface to interact with the
        Twitter API.

    Notes
    -----
    For this collector to work, you must set the following environment
    variables to the keys and tokens provided by Twitter:
    'TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_TOKEN'
    and 'TWITTER_ACCESS_TOKEN_SECRET'. See the docker-compose.yml file and set
    those variables in the proper env_file specified there.

    Refer to https://developer.twitter.com/en/docs/twitter-api/ and
    https://docs.tweepy.org/en/latest/ to know more about the limitations of
    this collection method.
    """

    def __init__(self):
        """
        It sets up the connection to the Twitter API using Tweepy.
        """

        auth = tweepy.OAuthHandler(
            settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET
        )
        auth.set_access_token(
            settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def collect(self, search_term, number_of_tweets):
        """
        This method performs the actual tweets collection.

        Parameters
        ----------
        search_term : str
            Term entered by the user in the search box.
        number_of_tweets : int
            Number of tweets the user requested to collect.

        Returns
        -------
        tweepy.SearchResults
            Iterable of tweepy.Status objects containing information about a
            tweet.
        """

        query = f'{search_term} -filter:retweets'
        cursor = tweepy.Cursor(
            self.api.search, q=query, tweet_mode='extended',
            result_type='recent', include_entities=False
        )
        return cursor.items(number_of_tweets)
