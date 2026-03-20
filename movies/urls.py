from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('movie/<int:movie_id>', views.MovieDetailView.as_view(), name='movie_detail'),
]