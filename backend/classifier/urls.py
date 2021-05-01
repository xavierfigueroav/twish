from django.urls import path

from .views import email
from .views import result
from .views import search


urlpatterns = [
    path('search', search),
    path('result', result),
    path('email', email),
]
