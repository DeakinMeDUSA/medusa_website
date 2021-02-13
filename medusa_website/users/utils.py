from django.http import JsonResponse
from django.middleware.csrf import get_token

from .serializers import UserSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": UserSerializer(user, context={"request": request}).data,
    }


# From https://fractalideas.com/blog/making-react-and-django-play-well-together-single-page-app-model/
def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


def ping(request):
    return JsonResponse({"result": "OK"})
