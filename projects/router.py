from django.urls import path
from projects import views
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
router.register(r'project', views.ProjectViewSet, basename='project')
router.register(r'invitations', views.InvitationViewSet, basename='invitations')
urlpatterns = router.urls
