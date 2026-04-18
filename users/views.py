from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from movies.models import Movie, Genre
from users.forms import CustomUserLoginForm, CustomUserCreationForm, CustomUserUpdateForm
from users.models import UserMovieInteraction


# Create your views here.
@login_required(login_url="/users/login/")
def profile(request):
    if request.method == "POST":
        form = CustomUserUpdateForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = CustomUserUpdateForm(instance=request.user)

    user = request.user

    interactions = UserMovieInteraction.objects.filter(user=user)

    watched_count = interactions.filter(is_watched=True).count() #количество просмотренных фильмов

    watched_movies = Movie.objects.filter(
        usermovieinteraction__user=user,
        usermovieinteraction__is_watched=True
    ).distinct() #список просмотренных фильмов

    watched_movie_ids = list(interactions.filter(is_watched=True).values_list('movie_id', flat=True)) #список ID просмотренных фильмов

    liked_count = interactions.filter(is_liked=True).count()

    all_genres = Genre.objects.all()
    favorite_genres = user.favorite_genres.all()

    context = {
        "title": f"Профиль - {request.user.first_name} {request.user.last_name}",
        "user": user,
        "form": form,
        "watched_count": watched_count,
        "liked_count": liked_count,
        "watched_movies": watched_movies,
        "watched_movie_ids": watched_movie_ids,
        "all_genres": all_genres,
        "favorite_genres": favorite_genres,
    }
    return render(request, "users/profile.html", context)



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


@login_required
def update_favorite_genres(request):
    if request.method == 'POST':
        genre_ids = request.POST.getlist('favorite_genres')



        # Очищаем текущие жанры и добавляем новые
        request.user.favorite_genres.clear()
        request.user.favorite_genres.add(*genre_ids)

        messages.success(request, 'Ваши любимые жанры обновлены!')

    return redirect('users:profile')

def logout_view(request):
    logout(request)

    return redirect('users:login')