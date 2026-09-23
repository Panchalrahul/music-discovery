from rest_framework import serializers
from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommendation

        fields = [
            'id',
            'user',
            'spotify_track_id',
            'track_name',
            'artist_name',
            'album_name',
            'track_url',
            'created_at',
        ]