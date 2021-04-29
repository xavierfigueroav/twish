import json

from django.conf import settings
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

from .storage import OverwriteableStorage
from .utils import logo_filename


class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True


class Predictor(BaseModel):
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        db_table = 'Predictor'

    def __str__(self):
        return f'{self.name} ({self.version})'

    def __repr__(self):
        return f'{self.name} ({self.version})'


class PredictionLabel(BaseModel):
    label = models.CharField(max_length=20)
    integer_label = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=100)
    predictor = models.ForeignKey(Predictor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PredictionLabel'

    def __str__(self):
        return f'{self.label} ({self.integer_label})'

    def __repr__(self):
        return f'{self.label} ({self.integer_label})'


class Tweet(BaseModel):
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
        return {
            'name': self.name,
            'description': self.description,
            'logo': self.logo.url,
            'about': self.about,
            'enable_email_notification': self.enable_email_notification,
            'allow_user_to_choose_predictor': self.allow_user_to_choose_predictor, # noqa
            'allow_user_to_choose_number_of_tweets': self.allow_user_to_choose_number_of_tweets, # noqa
            'default_predictor': self.default_predictor.name,
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with open(settings.APP_CONFIG_PATH, 'w') as config_file:
            json.dump(self.as_dict(), config_file, indent=4)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
