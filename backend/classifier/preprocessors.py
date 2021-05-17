"""
This module is meant to contain classes responsible for preparing data for
prediction.

Notes
-----
You are not required to create preprocessors at all, it depends a lot on your
prediction logic. However, if you need to perform several data preparation
steps/tasks before making actual predictions, you are encouraged to encapsulate
those routines in a class in here.
"""
import os
import re
import string

import joblib
import nltk
import numpy as np
import pandas as pd


class LogisticRegressionPreprocessor:
    """
    This class encapsulates the business logic to preprocess and prepare the
    raw tweets for the Logistic Regression predictor to make predictions.

    Attributes
    ----------
    regex_1 : SRE_Pattern
        Regular expression pattern to match top-level domains.
    regex_2 : SRE_Pattern
        Regular expression pattern to match protocol and domain names in URLs.
    trans_table : dict
        Mapping table to remove punctuations.
    processor_model : object
        Unpickled, trained TF-IDF vectorizer.
    """

    regex_1 = re.compile(r'\S+(\.)(com|net|ly|co|us|ec|gob)(\S?)+')
    regex_2 = re.compile(r'(http|facebook|twitter|bit|soundcloud|www|pic|#|@)\S+') # noqa
    trans_table = str.maketrans('', '', string.punctuation)

    def __init__(self):
        """
        This method loads the processor_model file by calling the method
        load_model and downloads the required NLTK module 'punkt'.
        """

        nltk.download('punkt')
        self.load_model()

    def load_model(self):
        """
        This method loads the pickled, trained TF-IDF vectorizer.
        """

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'models', 'example', 'tfidf.model') # noqa
        self.processor_model = joblib.load(file_path)

    def normalize_case(self, data):
        """
        This method normalizes the text case transforming it to lower case.

        Parameters
        ----------
        data : str
            Tweet text to normalize case.

        Returns
        -------
        str
            Lower-case tweet text.
        """

        return data.lower()

    def remove_hastags_mentions_links(self, data):
        """
        This method removes hashtags, mentions and links from data.

        Parameters
        ----------
        data : str
            Tweet text to remove hashtags, mentions and links from.

        Returns
        -------
        str
            Tweet text without hashtags, mentions and links.
        """

        data = LogisticRegressionPreprocessor.regex_1.sub('', data)
        data = LogisticRegressionPreprocessor.regex_2.sub('', data)
        return data

    def remove_punctuations(self, data):
        """
        This method removes puctuations from data.

        Parameters
        ----------
        data : list of str
            Collection of words in the tweet to remove puctuations from.

        Returns
        -------
        list of str
            Collection of words in the tweet excluding puctuations.
        """

        return [
            token.translate(LogisticRegressionPreprocessor.trans_table)
            for token in data
        ]

    def remove_numerics(self, data):
        """
        This method removes numeric characters from data.

        Parameters
        ----------
        data : list of str
            Collection of words in the tweet to remove numeric characters from.

        Returns
        -------
        list of str
            Collection of words in the tweet excluding numeric characters.
        """

        return [token for token in data if token.isalpha()]

    def remove_accents(self, data):
        """
        This method removes accents from data.

        Parameters
        ----------
        data : str
            Tweet text to remove accents from.

        Returns
        -------
        str
            Tweet text without accents.
        """

        data = data.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        data = data.replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')
        return data

    def remove_short_lines(self, data, short_line_words=3):
        """
        This method discrimitates short lines from not short lines.

        Parameters
        ----------
        data : list of str
            Collection of words in the tweet.

        short_line_words : int, default=3
            Number of words until which data is considered a short line.

        Returns
        -------
        list of str or np.nan
            If data is a short line, it returns np.nan, otherwise it returns
            data unmodified.
        """

        return data if len(data) > short_line_words else np.nan

    def tokenize(self, data):
        """
        This method splits data into words using a word tokenizer from NLTK.

        Parameters
        ----------
        data : str
            Tweet text to split into words.

        Returns
        -------
        list of str
            Tweet text split into words, collection of words.
        """

        return nltk.word_tokenize(data, language='spanish')

    def undo_tokenization(self, data):
        """
        This method joins words into a single string.

        Parameters
        ----------
        data : list of str
            Collection of words to join into a single string.

        Returns
        -------
        str or np.nan
            If data is np.nan, it returns data itself, otherwise it returns the
            words joined into a single string.
        """

        if data is np.nan:
            return np.nan
        return ' '.join(data)

    def preprocess(self, tweets):
        """
        This method orchestrates all of the tasks needed to successfully
        prepare tweets for prediction.

        Parameters
        ----------
        tweets : list of triples
            Collection of triples containing tweet information in the following
            order: tweet id, tweet date, tweet text.

        Returns
        -------
        None or triple of np.array
            If after preprocessing no tweets remain (which can happen when all
            the tweets are considered short lines), it returns None, otherwise
            it returns a triple of np.array in the following order:
            tweet identifiers, tweet dates, feature matrix to feed predictor.
        """

        data = pd.DataFrame(data=tweets, columns=['id', 'date', 'tweet'])
        data.tweet = data.tweet.apply(self.normalize_case)
        data.tweet = data.tweet.apply(self.remove_hastags_mentions_links)
        data.tweet = data.tweet.apply(self.remove_accents)
        data.tweet = data.tweet.apply(self.tokenize)
        data.tweet = data.tweet.apply(self.remove_punctuations)
        data.tweet = data.tweet.apply(self.remove_numerics)
        data.tweet = data.tweet.apply(self.remove_short_lines)
        data.tweet = data.tweet.apply(self.undo_tokenization)
        data = data[~data.tweet.isna()]

        if data.shape[0] != 0:
            features = self.processor_model.transform(data.tweet.values).todense() # noqa
            return data.id.values, data.date.values, features
