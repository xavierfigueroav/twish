import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import App
from .serializers import SearchSerializer


APP = App.objects.all()[0]


@api_view(['POST'])
def search(request):
    # TODO: Validate uniqueness of truncated_uuid
    request.data['truncated_uuid'] = uuid.uuid4().hex[:8]
    request.data['predictor'] = request.data.get(
        'predictor', APP.default_predictor.id
    )
    serializer = SearchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # TODO: Publish to task queue for further processing
    return Response(serializer.data)
