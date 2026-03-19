from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie
from .services.movie_service import download_and_save_poster


@receiver(post_save, sender=Movie)
def download_poster_on_create(sender, instance, created, **kwargs):
    """
    Скачиваем постер только если фильм создан впервые
    """
    if created:
        download_and_save_poster(instance)
