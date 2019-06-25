from django.urls import path, include
from .views import get_profile_picture


pictures_urls = [
    path('profile_images/<str:name>/', get_profile_picture),
]

urlpatterns = [
    path('images/', include(pictures_urls))
]
