from django.http import JsonResponse


# noinspection PyUnusedLocal
def ping(request):
    return JsonResponse({"result": "OK"})
