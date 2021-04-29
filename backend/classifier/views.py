import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import App
from .serializers import SearchSerializer
from .tasks import collect_tweets


@api_view(['POST'])
def search(request):
    APP = App.objects.all().get()
    # TODO: Validate uniqueness of truncated_uuid
    request.data['truncated_uuid'] = uuid.uuid4().hex[:8]
    request.data['predictor'] = request.data.get(
        'predictor', APP.default_predictor.id
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
