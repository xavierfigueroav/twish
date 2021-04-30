import uuid

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    return Response(serializer.data)
