import math
from django.core.management.base import BaseCommand
from movies.services.tmdb import tmdb_request
from movies.services.movie_service import save_movie_from_tmdb, download_and_save_poster

class Command(BaseCommand):
    help = "Fetch 2000 most popular and now playing movies from TMDB"

    def handle(self, *args, **options):
        self.stdout.write("Начало загрузки фильмов...")

        total_needed = 2000
        per_page = 20  # TMDB по умолчанию возвращает 20 фильмов на страницу

        endpoints = ["/movie/popular", "/movie/now_playing"]

        for endpoint in endpoints:
            page = 1
            while True:
                data = tmdb_request(endpoint, {"page": page})
                results = data.get("results", [])
                if not results:
                    break

                for movie_data in results:
                    # Получаем детальную информацию по фильму
                    from movies.services.tmdb import get_movie_detail
                    detail_data = get_movie_detail(movie_data["id"])
                    movie = save_movie_from_tmdb(detail_data)
                    download_and_save_poster(movie)

                    total_needed -= 1
                    if total_needed <= 0:
                        self.stdout.write("Загрузка завершена: достигнут лимит 2000 фильмов")
                        return

                page += 1
                total_pages = data.get("total_pages", 1)
                if page > total_pages:
                    break

        self.stdout.write("Загрузка завершена")