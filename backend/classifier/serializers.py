from rest_framework import serializers

from .models import Search


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['truncated_uuid', 'search_term', 'number_of_tweets', 'predictor'] # noqa
