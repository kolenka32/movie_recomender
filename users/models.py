from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre


# Create your models here.
class User(AbstractUser):
    favorite_movies = models.ManyToManyField(Movie, related_name='favorite_movies', blank=True)
    favorite_genres = models.ManyToManyField(Genre, related_name='favorite_genres', blank=True)
    liked_movies = models.ManyToManyField(Movie, related_name="liked_by", blank=True)
    disliked_movies = models.ManyToManyField(Movie, related_name="disliked_by", blank=True)

    def __str__(self):
        return self.username