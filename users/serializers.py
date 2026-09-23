from rest_framework import serializers
from .models import UserProfile, UserPreference


class UserPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPreference
        fields = ['genres', 'artists', 'moods']


class UserSerializer(serializers.ModelSerializer):

    genres = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    artists = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    moods = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'name',
            'email',
            'genres',
            'artists',
            'moods',
            'created_at',
        ]

    def create(self, validated_data):

        genres = validated_data.pop('genres')
        artists = validated_data.pop('artists')
        moods = validated_data.pop('moods')

        user = UserProfile.objects.create(
            **validated_data
        )

        UserPreference.objects.create(
            user=user,
            genres=genres,
            artists=artists,
            moods=moods
        )

        return user



class UserDetailSerializer(serializers.ModelSerializer):

    genres = serializers.SerializerMethodField()
    artists = serializers.SerializerMethodField()
    moods = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'name',
            'email',
            'genres',
            'artists',
            'moods',
            'created_at',
        ]

    def get_genres(self, obj):
        return obj.preferences.genres

    def get_artists(self, obj):
        return obj.preferences.artists

    def get_moods(self, obj):
        return obj.preferences.moods