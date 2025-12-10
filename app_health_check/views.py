from django.http import JsonResponse


def liveness(request):
    return JsonResponse({"status": "ok"})
