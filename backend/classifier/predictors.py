import os
import re
import string

import joblib
import nltk
import numpy as np
import pandas as pd

from .models import PredictionLabel


class Preprocessor:

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
        data = Preprocessor.regex_1.sub('', data)
        data = Preprocessor.regex_2.sub('', data)
        return data

    def remove_punctuations(self, data):
        return [token.translate(Preprocessor.trans_table) for token in data]

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


class Predictor:
    """
    This is the class you should customize to perform prediction and,
    more importantly, any io/memory-intensive task, such us loading
    model files. Why? Beacuse instances from this class are being cached
    in utils.py.

    This class should not be instantiated directly. You should call
    get_predictor (in utils.py) to pass through the cache. Take a look
    at tasks.py for an example.

    If you want to create your own class, make sure you modify get_predictor
    accordingly, unless you do not want to cache at all.
    """

    def __init__(self, predictor):
        self.predictor = predictor
        labels = PredictionLabel.objects.filter(predictor=self.predictor)
        self.labels = {label.integer_label: label for label in labels}
        self.preprocessor = Preprocessor()
        self.load_model()

    def load_model(self):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'models', 'example', 'logit.model') # noqa
        self.prediction_model = joblib.load(file_path)

    def predict(self, tweets):
        """
        This method performs the prediction tasks based on a list of tweets.

        It must return an iterable whose elements should be iterables
        containing three elements in the following order: the tweet id,
        the tweet date and the predicted label (instance of
        .models.PredictedLabel, taken from self.labels).

        If you want this method to return something different, you will need to
        modify tasks.py accordingly.
        """

        preprocessed_data = self.preprocessor.preprocess(tweets)
        result = []
        if preprocessed_data is not None:
            ids, dates, features = preprocessed_data
            prediction = self.prediction_model.predict(features)

            for i in range(ids.shape[0]):
                result.append((ids[i], dates[i], self.labels[prediction[i]]))
        return result
