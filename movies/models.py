from django.db import models
from django.contrib.postgres.indexes import GinIndex


class Genre(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.PositiveIntegerField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    adult = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    local_poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    local_backdrop = models.ImageField(upload_to="backdrops/", blank=True, null=True)

    class Meta:
        ordering = ["-release_date"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["release_date"]),

            GinIndex(
                fields=["title"],
                name="movie_title_trgm",
                opclasses=["gin_trgm_ops"]
            ),
        ]

    def __str__(self):
        return self.title

    @property
    def poster_url(self):
        poster_url_i = f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return poster_url_i

    @property
    def backdrop_url(self):
        backdrop_url_i = f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return backdrop_url_i
