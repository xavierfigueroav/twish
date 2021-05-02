from random import choice

from .models import PredictionLabel


class BasePredictor:

    def __init__(self, predictor):
        self.predictor = predictor
        self.labels = PredictionLabel.objects.filter(predictor=self.predictor)

    def predict(self, tweets):
        raise NotImplementedError()


class Predictor(BasePredictor):
    """
    This is the class you should customize to perform prediction and,
    more importantly, any io/memory-intensive task, such us loading
    model files. Why? Beacuse instances from this class are being cached
    in utils.py.

    This class should not be instantiated directly. You should call
    get_predictor from utils.py to pass through the cache. Take a look
    at tasks.py for an example.

    If you want to create your own class, make sure you modify get_predictor
    accordingly, unless you do not want to cache heavy files.
    """

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

        return [(id, choice(self.labels)) for id, date, _ in tweets]
