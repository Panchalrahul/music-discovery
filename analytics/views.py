from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import UserProfile
from activity.models import UserActivity
from recommendations.models import Recommendation
from collections import Counter


@api_view(['GET'])
def analytics_summary(request):

    total_users = UserProfile.objects.count()

    total_activities = UserActivity.objects.count()

    total_recommendations = Recommendation.objects.count()

    total_plays = UserActivity.objects.filter(
        action='play'
    ).count()

    total_likes = UserActivity.objects.filter(
        action='like'
    ).count()

    total_skips = UserActivity.objects.filter(
        action='skip'
    ).count()

    return Response({
        "total_users": total_users,
        "total_activities": total_activities,
        "total_recommendations": total_recommendations,
        "total_plays": total_plays,
        "total_likes": total_likes,
        "total_skips": total_skips
    })


@api_view(['GET'])
def analytics_trends(request):

    # Trending artists
    activities = UserActivity.objects.all()

    artist_names = []

    for activity in activities:
        artist_names.append(activity.artist_name)

    artist_counter = Counter(artist_names)

    trending_artists = []

    for artist, count in artist_counter.most_common():
        trending_artists.append({
            "artist": artist,
            "activity_count": count
        })

    # Trending genres
    users = UserProfile.objects.all()

    genre_names = []

    for user in users:
        try:
            genres = user.preferences.genres

            for genre in genres:
                genre_names.append(genre)

        except UserProfile.preferences.RelatedObjectDoesNotExist:
            pass

    genre_counter = Counter(genre_names)

    trending_genres = []

    for genre, count in genre_counter.most_common():
        trending_genres.append({
            "genre": genre,
            "user_count": count
        })

    return Response({
        "trending_artists": trending_artists,
        "trending_genres": trending_genres
    })


@api_view(['GET'])
def user_analytics(request, user_id):

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=404
        )

    total_activities = UserActivity.objects.filter(
        user=user
    ).count()

    total_plays = UserActivity.objects.filter(
        user=user,
        action='play'
    ).count()

    total_likes = UserActivity.objects.filter(
        user=user,
        action='like'
    ).count()

    total_skips = UserActivity.objects.filter(
        user=user,
        action='skip'
    ).count()

    return Response({
        "user_id": user_id,
        "total_activities": total_activities,
        "total_plays": total_plays,
        "total_likes": total_likes,
        "total_skips": total_skips
    })