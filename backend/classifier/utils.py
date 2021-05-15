import json

from django.conf import settings
from django.core.cache import cache
from django.utils.module_loading import import_string


PREDICTORS_DIR = 'classifier.predictors'


def logo_filename(instance, filename):
    return 'logo'


def get_predictor(predictor):
    """
    This method returns a predictors from predictors.py based on
    a .models.Predictor instance.

    If there exists a predictor instance in cache for the .models.Predictor
    received, it returns the cached instance, otherwise, it creates a new
    instance and cache it.
    """

    predictors = cache.get_or_set('PREDICTORS', {})
    if predictor.id not in predictors:
        GenericPredictor = import_string(f'{PREDICTORS_DIR}.{predictor.name}')
        predictors[predictor.id] = GenericPredictor(predictor)
        cache.set('PREDICTORS', predictors)
    return predictors[predictor.id]


def update_app_settings():
    from .models import App

    if App.objects.exists():
        app = App.objects.get()
        data = app.as_dict()
        cache.set('APP', app)
    else:
        data = {}
        cache.delete('APP')

    with open(settings.APP_CONFIG_PATH, 'w') as config_file:
        json.dump(data, config_file, indent=4)
