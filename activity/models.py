from django.db import models
from users.models import UserProfile


class UserActivity(models.Model):

    ACTION_CHOICES = [
        ('play', 'Play'),
        ('like', 'Like'),
        ('skip', 'Skip'),
    ]

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    spotify_track_id = models.CharField(max_length=100)
    track_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.track_name