from django.contrib import admin

from .models import App
from .models import PredictionLabel
from .models import Predictor

admin.site.register(App)
admin.site.register(Predictor)
admin.site.register(PredictionLabel)
