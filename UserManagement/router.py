from django.urls import path
from . import views
from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class CustomRouter(SimpleRouter):
    """
    A router for browsing user and managing self
    """
    routes = [
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                    'get': 'self_retrieve',
                    'post': 'create',
                    'patch': 'customize',
             },
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'create'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'detail'}
        ),

    ]


router = CustomRouter()
v = views.UserViewSet
router.register(r'', v)
urlpatterns = router.urls
print("Patterns", urlpatterns)
