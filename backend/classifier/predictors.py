import abc
import os

import joblib

from .preprocessors import LogisticRegressionPreprocessor


class AbstractPredictor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def predict(self, tweets):
        pass


class LogisticRegression(AbstractPredictor):
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
        from .models import PredictionLabel
        self.predictor = predictor
        labels = PredictionLabel.objects.filter(predictor=self.predictor)
        self.labels = {label.integer_label: label for label in labels}
        self.preprocessor = LogisticRegressionPreprocessor()
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
