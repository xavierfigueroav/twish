"""
This module contains the application models. These are classes to be used by
the Django ORM to provide a programming interface between the database and
the Django application.

The application models are:
    * App - It encapsulates information about appplication setting options.
    * Search - It encapsulates information about a search done by an app user.
    * Searcher - It encapsulates information about a user interested in being
    notified when the collection and classfication of a given search are
    finished.
    * Tweet - It encapsulates information about a tweet collected.
    * Predictor - It encapsulates information about a tweet predictor.
    * Prediction - It encapsulates information about a prediction made.
    * PredictionLabel - It encapsulates information about a label that may be
    predicted by a predictive model.
"""
from django.core.cache import cache
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

from .storage import OverwriteableStorage
from .utils import logo_filename
from .utils import update_app_settings


class BaseModel(SafeDeleteModel):
    """
    Abstact Model class that sets up django-safedelete policy.

    This class sets the _safedelete_policy attribute to SOFT_DELETE_CASCADE,
    which means that its subclasses' instances and all related objects will be
    automatically masked (and not deleted) when you call the delete() method.

    It is intended to be subclassed by all the models whose instances are
    not meant to be permanently deleted from database.

    Attributes
    ----------
    _safedelete_policy : int
        django-safedelete delete policy.

    Notes
    -----
    Refer to https://django-safedelete.readthedocs.io/ for further information
    on how django-safedelete works.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True


class Predictor(BaseModel):
    """
    This model encapsulates information about a tweet predictor.

    Attributes
    ----------
    name : str
        Name of the predictor. Max 30 characters.
    version : str
        Version of the predictor. Max 10 characters.
    description : str.
        Long description about the predictor. This may include hyperparameter
        values, validation technique, etc. Treat this as the predictor docs.
        Max 200 characters.
    active : bool, default=True
        When the app is configured to allow the user to choose the predictor
        to use and this field is True, this predictor is shown to the user,
        otherwise is not shown.
    """

    name = models.CharField(max_length=30)
    version = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        db_table = 'Predictor'

    def as_dict(self):
        """
        This method creates a Python-types representation of the Predictor
        model.

        It includes a list of PredictionLabel (represented with pure Python
        types, too) to enrich predictor information.

        Returns
        -------
        dict
            Predictor information represented with pure Python data types.
        """

        labels = []
        for label in PredictionLabel.objects.filter(predictor=self):
            labels.append({
                'label': label.label,
                'integer_label': label.integer_label,
                'description': label.description
            })

        return {
            'name': self.name,
            'version': self.version,
            'description': self.version,
            'labels': labels
        }

    def __str__(self):
        return f'{self.name} ({self.version})'

    def __repr__(self):
        return f'{self.name} ({self.version})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_app_settings()
        self.delete_predictor_from_cache()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        update_app_settings()
        self.delete_predictor_from_cache()

    # FIXME: cache is not being updated when running cache.set here.
    # cache from .models and cache from .utils seem to be different.
    # This may be a sign of being running two django instances.
    # Check backend and celery services in docker-compose.yml.
    def delete_predictor_from_cache(self):
        """
        This method removes a Predictor (from predictors.py) instance
        from cache if its id matches this model id.

        It is intended to be used when predictor-related information changes,
        which includes creating/updating/deleting instances of the models
        Predictor and PredictionLabel.
        """

        predictors = cache.get_or_set('PREDICTORS', {})
        if self.id in predictors:
            del predictors[self.id]
            cache.set('PREDICTORS', predictors)


class PredictionLabel(BaseModel):
    """
    This model encapsulates information about a label that may be predicted
    by a predictive model.

    Attributes
    ----------
    label : str
        Human-readable label to be shown to the user. Max 20 characters.
    integer_label : int
        Integer label to match actual model prediction and the instance of
        this model.
    description : str
        Description of the label. Try to answer what this labels means.
        Treat this as the label docs. Max 100 characters.
    predictor : Predictor
        The predictor that may predict this label.
    """

    label = models.CharField(max_length=20)
    integer_label = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=100)
    predictor = models.ForeignKey(Predictor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PredictionLabel'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_app_settings()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        update_app_settings()

    def __str__(self):
        return f'{self.label} ({self.integer_label})'

    def __repr__(self):
        return f'{self.label} ({self.integer_label})'


class Tweet(BaseModel):
    """
    This model encapsulates information about tweets collected.

    Attributes
    ----------
    id : str
        Tweet identifier as provided by Twitter. Max 30 characters.
    date : datetime
        Tweet publishing date as provided by Twitter.
    predictors : QuerySet<Predictor>
        Collection of predictors that have made predictions for this tweet.
        This field represents a many-to-many relationship, which uses the
        Prediction model as intermediate model/table.
    """

    id = models.CharField(max_length=30, primary_key=True)
    date = models.DateTimeField()
    predictors = models.ManyToManyField(Predictor, through='Prediction')

    class Meta:
        db_table = 'Tweet'

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class Prediction(BaseModel):
    """
    This model encapsulates information about a label prediction for a tweet.

    Attributes
    ----------
    predictor : Predictor
        The predictor that performed the prediction.
    tweet : Tweet
        The tweet for which the prediction was made.
    label : PredictionLabel
        The label predicted.
    date : datetime
        Date when the prediction was made/stored.
    """

    predictor = models.ForeignKey(Predictor, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    label = models.ForeignKey(PredictionLabel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Prediction'
        unique_together = ('predictor', 'tweet')

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return str(self.label)


class Search(BaseModel):
    """
    This model encapsulates information about a search done by an app user.

    Attributes
    ----------
    truncated_uuid : str
        Random UUID truncated to 8 characters. It identifies the search in a
        user-friendly way, without exposing incremental indentifiers. The
        result of the collection and prediction is identified using this value.
        Max 8 characters.
    search_term : str
        Term entered by the user in the search box. Max 100 characters.
    date : models.DateTimeField
        Date when the user did the search.
    number_of_tweets :int
        Number of tweets the user requested to collect.
    empty : bool, default=False
        Set to True when no tweets were found for the search term,
        otherwise False.
    predictor : Predictor
        The predictor to used for the tweets collected in this search.
        If the app is not configured to allow the user to choose the predictor,
        it defaults to the default predictor set in the App model instance.
    tweets : Queryset<Tweet>
        Collection of tweets found in this search. This field represents a
        many-to-many relationship between Search and Tweet.
    """

    truncated_uuid = models.CharField(max_length=8, db_index=True)
    search_term = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    number_of_tweets = models.PositiveIntegerField()
    empty = models.BooleanField(default=False, blank=True)
    predictor = models.ForeignKey(Predictor, on_delete=models.CASCADE)
    tweets = models.ManyToManyField(Tweet)

    class Meta:
        db_table = 'Search'

    def __str__(self):
        return self.search_term

    def __repr__(self):
        return self.search_term


class Searcher(BaseModel):
    """
    This model encapsulates information about the user interested in being
    notified when the collection and classfication of a given search are
    finished.

    Attributes
    ----------
    name : str
        Name of the user. Max 50 characters.
    email : str
        Email of the user. This email address is used to notify the user.
    search : Search
        the search which the user is interested in.
    """

    name = models.CharField(max_length=50)
    email = models.EmailField()
    search = models.ForeignKey(Search, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Searcher'

    def __str__(self):
        return f'{self.name} ({self.email})'

    def __repr__(self):
        return f'{self.name} ({self.email})'


class App(models.Model):
    """
    This model encapsulates information about the application itself.

    It is intented to store configuration parameters. There must be
    only one instance of this model at a time.

    Attributes
    ----------
    name : str
        The name of the application. This name is set as the page title. Max 50
        characters.
    description : str
        Short description of the application. This description is set as the
        page meta description.
    about : str
        Long description of the application. It is shown to the user in the
        About page of the application.
    logo : models.ImageField, default=None
        Logo of the application. It is shown at the top of the site. If None,
        Twish logo is used.
    enable_email_notification : bool, default=False
        If True, the user can register their name and email to be notified
        when a search cicle (collection/classification) is finished. If False,
        the user is not shown this option in the app.
    allow_user_to_choose_predictor : bool, default=False
        If True, the user can choose the predictor to use for their search.
        If False, default_predictor is used to make predictions.
    allow_user_to_choose_number_of_tweets : bool, default=False
        If True, the user can choose the number of tweets to collect. If False,
        the user is not shown this option in the app and no limit is set for
        the amount of tweets to collect.
    default_predictor : Predictor
        The predictor to use when allow_user_to_choose_predictor is False.
    """

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    about = models.TextField()
    logo = models.ImageField(
        upload_to=logo_filename,
        storage=OverwriteableStorage,
        null=True, blank=True
    )
    enable_email_notification = models.BooleanField(default=False, blank=True)
    allow_user_to_choose_predictor = models.BooleanField(
        default=False, blank=True
    )
    allow_user_to_choose_number_of_tweets = models.BooleanField(
        default=False, blank=True
    )
    default_predictor = models.OneToOneField(
        Predictor, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = 'App'

    def as_dict(self):
        """
        This method creates a Python-types representation of the App model.

        Returns
        -------
        dict
            App information represented with pure Python data types.
        """

        return {
            'name': self.name,
            'description': self.description,
            'logo': self.logo.url if self.logo else None,
            'about': self.about,
            'enable_email_notification': self.enable_email_notification,
            'allow_user_to_choose_number_of_tweets': self.allow_user_to_choose_number_of_tweets, # noqa
            'predictor': self.default_predictor.as_dict() if self.default_predictor else None, # noqa
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_app_settings()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        update_app_settings()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
