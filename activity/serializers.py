from rest_framework import serializers
from .models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivity
        fields = [
            'id',
            'user',
            'spotify_track_id',
            'track_name',
            'artist_name',
            'action',
            'created_at',
        ]