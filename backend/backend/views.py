from django.http import HttpResponse, JsonResponse
from django.views import View

class HelloWorld(View):
    def get(self, request):
        return JsonResponse({"message":"Hello-world"})