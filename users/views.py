from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required(login_url="/users/login/")
def profile(request):

    context = {
        "title": f"Профиль - {request.user.first_name} {request.user.last_name}",
    }
    return render(request, "user/profile.html", context)