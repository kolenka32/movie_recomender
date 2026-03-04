from django.core.management.base import BaseCommand
from movies.services.bulk_import_service import fetch_bulk_movies


class Command(BaseCommand):
    help = "Import 2000 popular and new movies from TMDB"

    def handle(self, *args, **options):
        total = fetch_bulk_movies(limit=2000)
        self.stdout.write(self.style.SUCCESS(f"Импортировано фильмов: {total}"))