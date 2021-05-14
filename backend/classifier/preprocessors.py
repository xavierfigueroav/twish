import os
import re
import string

import joblib
import nltk
import numpy as np
import pandas as pd


class LogisticRegressionPreprocessor:

    regex_1 = re.compile(r'\S+(\.)(com|net|ly|co|us|ec|gob)(\S?)+')
    regex_2 = re.compile(r'(http|facebook|twitter|bit|soundcloud|www|pic|#|@)\S+') # noqa
    trans_table = str.maketrans('', '', string.punctuation)

    def __init__(self):
        nltk.download('punkt')
        self.load_model()

    def load_model(self):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'models', 'example', 'tfidf.model') # noqa
        self.processor_model = joblib.load(file_path)

    def normalize_case(self, data):
        return data.lower()

    def remove_hastags_mentions_links(self, data):
        data = LogisticRegressionPreprocessor.regex_1.sub('', data)
        data = LogisticRegressionPreprocessor.regex_2.sub('', data)
        return data

    def remove_punctuations(self, data):
        return [
            token.translate(LogisticRegressionPreprocessor.trans_table)
            for token in data
        ]

    def remove_numerics(self, data):
        return [token for token in data if token.isalpha()]

    def remove_accents(self, data):
        data = data.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        data = data.replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')
        return data

    def remove_short_lines(self, data, short_line_words=3):
        return data if len(data) > short_line_words else np.nan

    def tokenize(self, data):
        return nltk.word_tokenize(data, language='spanish')

    def undo_tokenization(self, data):
        if data is np.nan:
            return np.nan
        return ' '.join(data)

    def preprocess(self, tweets):
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
