from django.http import JsonResponse, HttpRequest
from django.views import View

class LivenessView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"status": "ok"})