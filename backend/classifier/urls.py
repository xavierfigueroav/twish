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
