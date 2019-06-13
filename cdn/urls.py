from django.urls import path, include
from .views import get_public_image


pictures_urls = [
    path('profile_pictures/<str:name>/', get_public_image),
]

urlpatterns = [
    path('pictures/', include(pictures_urls))
]
