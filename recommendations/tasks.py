from celery import shared_task

from users.models import UserProfile
from recommendations.models import Recommendation
from recommendations.spotify import get_recommendations_from_spotify

import redis
from django.conf import settings


@shared_task
def test_task():
    print("Celery task is working!")
    return "Task completed"


@shared_task
def refresh_recommendations_task(user_id):

    user = UserProfile.objects.get(id=user_id)

    preferences = user.preferences

    songs = get_recommendations_from_spotify(
        preferences.genres,
        preferences.artists,
        preferences.moods
    )

    Recommendation.objects.filter(
        user=user
    ).delete()

    for song in songs:

        Recommendation.objects.create(
            user=user,
            spotify_track_id=song["spotify_track_id"],
            track_name=song["track_name"],
            artist_name=song["artist_name"],
            album_name=song["album_name"],
            track_url=song["track_url"]
        )

    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )

    cache_key = f"recommendations_user_{user_id}"

    redis_client.delete(cache_key)

    print("Recommendations refreshed successfully")

    return "Recommendations refreshed successfully"


@shared_task
def refresh_all_users_task():

    users = UserProfile.objects.all()

    for user in users:
        refresh_recommendations_task.delay(user.id)

    return "All users recommendation refresh started"