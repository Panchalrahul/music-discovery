from django.urls import path
from .views import create_activity


urlpatterns = [
    path('', create_activity),
]