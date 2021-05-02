from django.core.cache import cache


def logo_filename(instance, filename):
    return 'logo'


def get_predictor(predictor):
    """
    This method returns a .predictors.Predictor instance based on
    a .models.Predictor instance.

    If there exists a .predictors.Predictor instance in cache for
    the .models.Predictor received, it returns the cached instance,
    otherwise, it creates a new instance.
    """
    from .predictors import Predictor
    predictors = cache.get_or_set('PREDICTORS', {})
    if predictor.id not in predictors:
        predictors[predictor.id] = Predictor(predictor)
        cache.set('PREDICTORS', predictors)
    return predictors[predictor.id]
