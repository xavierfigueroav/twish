from django.urls import path

from .views import result
from .views import search


urlpatterns = [
    path('result', result),
    path('search', search),
]
