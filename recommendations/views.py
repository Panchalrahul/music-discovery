import redis
import json

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from users.models import UserProfile

from .serializers import RecommendationSerializer
from .tasks import refresh_recommendations_task
from .models import Recommendation


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


@api_view(['POST'])
def refresh_recommendations(request, user_id):

    try:
        UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    refresh_recommendations_task.delay(user_id)

    return Response(
        {
            "message": "Recommendation refresh started"
        },
        status=status.HTTP_202_ACCEPTED
    )


@api_view(['GET'])
def get_recommendations(request, user_id):

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    cache_key = f"recommendations_user_{user_id}"

    cached_data = redis_client.get(cache_key)

    if cached_data:
        return Response(
            json.loads(cached_data),
            status=status.HTTP_200_OK
        )

    recommendations = Recommendation.objects.filter(
        user=user
    )

    serializer = RecommendationSerializer(
        recommendations,
        many=True
    )

    data = serializer.data

    redis_client.set(
        cache_key,
        json.dumps(data),
        ex=300
    )

    return Response(
        data,
        status=status.HTTP_200_OK
    )