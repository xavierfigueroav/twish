"""
This module contains the views reponsible for handling the requests received by
the API.

View list:
    * search - It triggers the asynchronous tweet collection task.
    * result - It returns the search and classification results of a given
    search.
    * email - It saves the name and email of a user interested in being
    notified when the collection and prediction process of a given search
    completes.
    * search_history - It returns all the searches for which tweets have been
    found and were classified successfuly.
"""
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
    """
    View to trigger the asynchronous tweet collection task. This view is
    called when the user uses the search box in the application GUI.

    Parameters
    ----------
    request : Request
        Information about the request made. The request body must contain the
        fields search_term and number_of_tweets, and may contain predictor if
        the user is allowed to choose the predictor to use.

    Returns
    -------
    Response
        The response status code is 200 and its body contains the Search
        instance data as validated by the SearchSerializer.
    """

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
    """
    View to get the search and classification results of a given search.

    Parameters
    ----------
    request : Request
        Information about the request made. The request body must contain the
        field search_id.

    Returns
    -------
    Response
        If the search_id received does not exist in database, the response
        status code is 404 and its body contains an error message.
        If the search_id received does exist, three cases may happen:
        1. Tweets were found for the given search term and the prediction
        process is completed: the response status code is 200 and its body
        contains a dictionary of tweets grouped by label.
        2. Tweets were found for the given search term, but the prediction
        process is not completed yet: the response status code is 200 and
        its body contains a message and a processing flag set to True, both
        indicating that processing is not completed yet.
        3. No tweets were found for the given search term: the response status
        code is 200 and its body contains a message and processing flag set to
        False, both indicating that processing was already completed.
    """

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
    """
    View to save the name and email of a user interested in being notified
    when the collection and prediction process of a given search completes.

    Parameters
    ----------
    request : Request
        Information about the request made. The request body must contain the
        fields name, email and search.

    Returns
    -------
    Response
        If the search received does not exist, the response status code is 404
        and its body contains an error message. If the search received does
        exist, the response status code is 200 and its body contains the
        Searcher instance data as validated by the SearcherSerializer.
    """

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


# TODO: Add support for pagination
@api_view(['GET'])
def search_history(request):
    """
    View to get all the searches for which tweets have been found and were
    classified successfuly. This view is called when the user browses the
    search history page.

    Parameters
    ----------
    request : Request
        Information about the request made.

    Returns
    -------
    Response
        The response status code is 200 and its body contains a list of Search
        instances data as validated by the SearchSerializer.
    """

    search_set = Search.objects.exclude(tweets=None).order_by('-date')
    serializer = SearchSerializer(search_set, many=True)
    return Response(serializer.data)
