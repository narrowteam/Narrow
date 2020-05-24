from django.http import HttpResponse
from PIL import Image
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from . import config as cdn_config
import os

# Only an prototype, will be fixed to more real life, secure solution

# @api_view(['get'])
# @permission_classes(IsAuthenticated)
# def get_profile_picture(request, name=None):
#     try:
#         path = cdn_config.PROFILE_IMAGES_PATH
#         path = path[path.find(settings.CDN_DOMAIN) + len(settings.CDN_DOMAIN):].strip('/')
#         with open(os.path.dirname(Narrow.__file__)[:-7] + '/' + path, "rb") as f:
#             return HttpResponse(f.read(), content_type="image/jpeg")
#     except IOError:
#         red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
#         response = HttpResponse(content_type="image/jpeg")
#         red.save(response, "JPEG")
#         return response



@api_view(['get'])
@permission_classes((IsAuthenticated, ))
def get_profile_picture(request, name=None):
    # try:
        pic_path = settings.CDN_ROOT + os.path.join(cdn_config.PROFILE_IMAGES_PATH, name)
        with open(pic_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    # except IOError:
    #     red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    #     response = HttpResponse(content_type="image/jpeg")
    #     red.save(response, "JPEG")
    #     return response
