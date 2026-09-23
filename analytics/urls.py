from django.urls import path
from .views import analytics_summary , analytics_trends , user_analytics


urlpatterns = [
    path('summary/', analytics_summary ),
    path('trends/', analytics_trends ),
    path('user/<int:user_id>/', user_analytics ),
]