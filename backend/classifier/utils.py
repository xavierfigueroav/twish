"""
This module defines some utility functions to use throughout the application.

Function list:
    * logo_filename - It is called to obtain the upload path of the app logo.
    * get_predictor - It returns and caches the corresponding predictive model
    (from predictors.py) instance for a given Predictor model instance.
    * update_app_settings - It updates the single App instance in cache and
    dumps its information to disk as a JSON file.
"""
import json

from django.conf import settings
from django.core.cache import cache
from django.utils.module_loading import import_string


PREDICTORS_DIR = 'classifier.predictors'


def logo_filename(instance, filename):
    """
    This function will be called by a file storage system to obtain the upload
    path (including the filename) of the app logo. It is set as the upload_to
    attribute for the logo ImageField in the App model.

    Parameters
    ----------
    instance : App
        The instance of the model where the ImageField is defined.
    filename : str
        The filename that was originally given to the image file when
        uploading.

    Returns
    -------
    str
        In spite of filename, 'logo' is always returned.

    Notes
    -----
    For further information on how this function is used by Django, refer to
    https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.FileField.upload_to
    """

    return 'logo'


def get_predictor(predictor):
    """
    It returns the corresponding predictive model (from predictors.py)
    instance for the Predictor model instance received and caches it.

    Parameters
    ----------
    predictor : Predictor
        Predictor chosen by the user when requesting the search and
        classification through the application GUI.

    Returns
    -------
    AbstractPredictor
        Predictor (from predictors.py) instance to make predictions. If there
        exists an instance in cache for the predictor received, it returns it,
        otherwise it creates a new one, caches it and returns it.

    Raises
    ------
    ModuleNotFoundError
        If the name attribute of the parameter predictor does not match any
        class name in the module predictors.py.
    """

    predictors = cache.get_or_set('PREDICTORS', {})
    if predictor.id not in predictors:
        GenericPredictor = import_string(f'{PREDICTORS_DIR}.{predictor.name}')
        predictors[predictor.id] = GenericPredictor(predictor)
        cache.set('PREDICTORS', predictors)
    return predictors[predictor.id]


def update_app_settings():
    """
    This function updates the single App instance in cache and dumps its
    information to disk as a JSON file.
    """

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
