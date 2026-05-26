from django.http import JsonResponse, HttpRequest
from django.views import View


class LivenessView(View):
    """
    Simple liveness endpoint for health checks.

    Used by load balancers, orchestration systems, or monitoring tools
    to verify that the application process is running and responsive.
    """
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"status": "ok"})