"""
This module is meant to contain classes that encapsulate prediction logic,
ranging from data preprocessing to the actual inference.

Notes
-----
Instances of classes in here are cached if you call get_predictor (utils.py)
instead of instantiating them directly. This is done to mitigate the cost of
loading (likely) heavy model files for every prediction request.
"""
import abc
import os

import joblib

from .preprocessors import LogisticRegressionPreprocessor


class AbstractPredictor(metaclass=abc.ABCMeta):
    """
    Abstract class which your custom predictors must subclass from.

    Notes
    -----
    You must register a Predictor model instance from the Django Admin
    interface and its name field must match your custom predictor class' name
    for the system to use it to make predictions.
    """

    @abc.abstractmethod
    def predict(self, tweets):
        """
        Method responsible for orchestrating all the needed data preparation
        tasks and the subsequent prediction.

        Parameters
        ----------
        tweets : list of triples
            Collection of triples containing tweet information in the following
            order: tweet id, tweet date, tweet text.

        Returns
        -------
        list of triples
            Collection of triples containing tweet and prediction information
            in the following order: tweet id, tweet date,
            tweet predicted label (instance of PredictionLabel).

        Notes
        -----
        Even though this abstract class forces you to implement the method
        predict, it does not force you to follow the parameter and return
        values format described in these docs. However, you are strongly
        encouraged to follow it to avoid further changes in the codebase.
        """

        pass


class LogisticRegression(AbstractPredictor):
    """
    Logistic Regression model and all the needed business logic for it to make
    predictions.

    Attributes
    ----------
    predictor : Predictor
        Corresponding Predictor model instance related to the actual
        prediction_model.
    labels : dict
        Collection of labels where each key is an integer that may be predicted
        by prediction_model and each value is its corresponding PredictionLabel
        instance.
    preprocessor : LogisticRegressionPreprocessor
        Responsible for preprocessing the tweets collected before passing them
        into the prediction model.
    prediction_model : object
        Unpickled, trained Logistic Regression model responsible for making
        predictions.
    """

    def __init__(self, predictor):
        """
        This method initializes the attributes predictor, label and
        preprocessor. It also loads the required model file by calling the
        method load_model.

        Parameters
        ----------
        predictor : Predictor
            Django representation of the actual predictive model.
        """

        from .models import PredictionLabel
        self.predictor = predictor
        labels = PredictionLabel.objects.filter(predictor=self.predictor)
        self.labels = {label.integer_label: label for label in labels}
        self.preprocessor = LogisticRegressionPreprocessor()
        self.load_model()

    def load_model(self):
        """
        This method loads the pickled, trained predictive model.
        """

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'models', 'example', 'logit.model') # noqa
        self.prediction_model = joblib.load(file_path)

    def predict(self, tweets):
        """
        Method responsible for orchestrating all the needed data preparation
        tasks and the subsequent prediction.

        Parameters
        ----------
        tweets : list of triples
            Collection of triples containing tweet information in the following
            order: tweet id, tweet date, tweet text.

        Returns
        -------
        list of triples
            Collection of triples containing tweet and prediction information
            in the following order: tweet id, tweet date,
            tweet predicted label (instance of PredictionLabel).
        """

        preprocessed_data = self.preprocessor.preprocess(tweets)
        result = []
        if preprocessed_data is not None:
            ids, dates, features = preprocessed_data
            prediction = self.prediction_model.predict(features)

            for i in range(ids.shape[0]):
                result.append((ids[i], dates[i], self.labels[prediction[i]]))
        return result
