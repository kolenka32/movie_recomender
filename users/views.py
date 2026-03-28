from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from users.forms import CustomUserLoginForm, CustomUserCreationForm


# Create your views here.
@login_required(login_url="/users/login/")
def profile(request):

    context = {
        "title": f"Профиль - {request.user.first_name} {request.user.last_name}",
    }
    return render(request, "users/profile.html", context)

def edit_profile(request):
    return render(request, "users/edit_profile.html")



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return TemplateResponse(request, 'users/register.html', {'form': form, 'title': 'Регистрация'})


def login_view(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:profile')
        else:
            print(form.errors)
    else:
        form = CustomUserLoginForm()

    return render(request, 'users/login.html', {'form': form, 'title': 'Вход'})




    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)

    return redirect('users:login')