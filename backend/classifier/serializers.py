from rest_framework import serializers

from .models import Search
from .models import Searcher


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search
        fields = ['truncated_uuid', 'search_term', 'number_of_tweets', 'predictor'] # noqa


class SearcherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Searcher
        fields = ['name', 'email']
