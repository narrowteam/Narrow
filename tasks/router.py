from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
router.register(r'', views.TaskViewSet, basename='')
urlpatterns = router.urls
