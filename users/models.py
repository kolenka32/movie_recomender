from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre


# Create your models here.

class UserMovieInteraction(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    is_liked = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    is_watched = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "movie"),)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    favorite_genres = models.ManyToManyField(Genre, related_name='favorite_genres', blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True, unique=True)


    def __str__(self):
        return self.username