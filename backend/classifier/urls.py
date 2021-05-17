"""
This module exposes the urlpatterns variable which defines the routes (and its
respective views) the application accepts.
"""
from django.urls import path

from .views import email
from .views import result
from .views import search
from .views import search_history


urlpatterns = [
    path('search', search),
    path('result', result),
    path('email', email),
    path('search_history', search_history),
]
