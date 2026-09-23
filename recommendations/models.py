from django.db import models
from users.models import UserProfile


class Recommendation(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    spotify_track_id = models.CharField(max_length=100)
    track_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)

    album_name = models.CharField(
        max_length=200,
        blank=True
    )

    track_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.track_name