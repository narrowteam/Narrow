from django.http import HttpResponse
from PIL import Image
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import Narrow, os

# Only an prototype, will be fixed to more real life, secure solution

@permission_classes((AllowAny,))
def get_public_image(request, name=None):
    # try:
    path = request.build_absolute_uri()
    path = path[path.find(settings.CDN_DOMAIN) + len(settings.CDN_DOMAIN):].strip('/')
    with open(os.path.dirname(Narrow.__file__)[:-7] + '/' + path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")
    # except IOError:
    #     red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    #     response = HttpResponse(content_type="image/jpeg")
    #     red.save(response, "JPEG")
    #     return response


