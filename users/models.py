from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserPreference(models.Model):
    user = models.OneToOneField(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='preferences'
    )

    genres = models.JSONField(default=list)
    artists = models.JSONField(default=list)
    moods = models.JSONField(default=list)

    def __str__(self):
        return self.user.name