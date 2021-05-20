"""
This module contains serializers to convert Django model instances to native
Python datatypes and vice versa.
"""
from rest_framework import serializers

from .models import Search
from .models import Searcher


class SearchSerializer(serializers.ModelSerializer):
    """
    Serializer to convert Search model instances to native Python datatypes
    and vice versa.
    """

    class Meta:
        model = Search
        fields = [
            'truncated_uuid', 'search_term', 'number_of_tweets', 'predictor', 'date' # noqa
        ]


class SearcherSerializer(serializers.ModelSerializer):
    """
    Serializer to convert Searcher model instances to native Python datatypes
    and vice versa.
    """

    class Meta:
        model = Searcher
        fields = ['name', 'email']
