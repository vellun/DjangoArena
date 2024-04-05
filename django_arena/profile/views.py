from django.http import HttpResponse
from profile.models import CustomProfile, Problem


def profile_page(request):
    if request.user.is_authenticated:
        solved_tasks = CustomProfile.objects.prefetch_related("problem")
        return HttpResponse(content=solved_tasks, status=200)
    return HttpResponse(content="please, login", status=200)
