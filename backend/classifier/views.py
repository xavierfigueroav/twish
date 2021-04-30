import uuid

from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Prediction
from .models import Search
from .serializers import SearchSerializer
from .tasks import collect_tweets
from .utils import app_information


@api_view(['POST'])
def search(request):
    app = cache.get_or_set('APP', app_information)
    # TODO: Validate uniqueness of truncated_uuid
    request.data['truncated_uuid'] = uuid.uuid4().hex[:8]
    request.data['predictor'] = request.data.get(
        'predictor', app.default_predictor.id
    )
    serializer = SearchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    search_instance = serializer.save()
    collect_tweets.delay(
        search_instance.id,
        search_instance.search_term,
        search_instance.number_of_tweets
    )
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def result(request):
    search_id = request.data.get('search_id')
    try:
        search_instance = Search.objects.get(truncated_uuid=search_id)
    except Search.DoesNotExist:
        message = {
            'search_id': [f'Invalid id {search_id} - search does not exist.']
        }
        return Response(message, status=status.HTTP_404_NOT_FOUND)

    if search_instance.empty:
        # TODO: Hide search after this condition is True for the first time
        search_term = search_instance.search_term
        message = {
            'tweets': [
                f"Unfortunately, we did not found tweets for '{search_term}'."
            ]
        }
        return Response(message, status=status.HTTP_204_NO_CONTENT)

    tweets = search_instance.tweets.all()

    if len(tweets) == 0:
        search_term = search_instance.search_term
        message = {
            'tweets': [
                f"Tweets collection and classification for '{search_term}' \
have not been completed yet."
            ]
        }
        return Response(message, status=status.HTTP_204_NO_CONTENT)

    data = dict()
    for tweet in tweets:
        prediction = Prediction.objects.get(
            predictor=search_instance.predictor, tweet=tweet
        )
        data[prediction.label.label] = data.get(prediction.label.label, [])
        data[prediction.label.label].append(tweet.id)

    return Response(data)
