from django.urls import path, include
from projects import views
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
router.register(r'project', views.ProjectViewSet, basename='project')
router.register(r'invitations', views.InvitationViewSet, basename='invitations')
urlpatterns = router.urls + [path('project_tasks/<int:project_id>/', include(('tasks.router', 'tasks'),  namespace='tasks'))]

