from django.core.cache import cache
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

from .storage import OverwriteableStorage
from .utils import logo_filename
from .utils import update_app_settings


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

    def as_dict(self):
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
        predictors = cache.get_or_set('PREDICTORS', {})
        if self.id in predictors:
            del predictors[self.id]
            cache.set('PREDICTORS', predictors)


class PredictionLabel(BaseModel):
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
