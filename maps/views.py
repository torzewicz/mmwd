from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("<h1>Hi</h1>")


def dupa(requet):
    return JsonResponse()