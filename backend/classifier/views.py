import uuid

from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import App
from .models import Prediction
from .models import Search
from .serializers import SearcherSerializer
from .serializers import SearchSerializer
from .tasks import collect_tweets


@api_view(['POST'])
def search(request):
    app = cache.get_or_set('APP', App.objects.get)
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


@api_view(['POST'])
def result(request):
    search_id = request.data.get('search_id')
    try:
        search_instance = Search.objects.get(truncated_uuid=search_id)
    except Search.DoesNotExist:
        data = {
            'detail': f'Invalid id {search_id} - search does not exist.',
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    search_term = search_instance.search_term

    if search_instance.empty:
        # TODO: Hide search after this condition is True for the first time
        data = {
            'detail': f"Unfortunately, we did not found tweets for '{search_term}'.", # noqa
            'search_term': search_term,
            'processing': False
        }
        return Response(data)

    tweets = search_instance.tweets.all()

    if len(tweets) == 0:
        data = {
            'detail': f"Tweets collection and classification for '{search_term}' \
have not been completed yet.",
            'search_term': search_term,
            'processing': True
        }
        return Response(data)

    data = dict()
    for tweet in tweets:
        prediction = Prediction.objects.get(
            predictor=search_instance.predictor, tweet=tweet
        )
        data[prediction.label.label] = data.get(prediction.label.label, [])
        data[prediction.label.label].append(tweet.id)

    data['search_term'] = search_term

    return Response(data)


@api_view(['POST'])
def email(request):
    serializer = SearcherSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    search_truncated_uuid = request.data.get('search')
    try:
        search_instance = Search.objects.get(
            truncated_uuid=search_truncated_uuid
        )
    except Search.DoesNotExist:
        message = {
            'search_id': [
                f'Invalid id {search_truncated_uuid} - search does not exist.'
            ]
        }
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    serializer.save(search=search_instance)
    return Response(serializer.data)
