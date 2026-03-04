from movies.services.tmdb import tmdb_request, get_movie_detail
from movies.services.movie_service import save_movie_from_tmdb, download_and_save_poster


def fetch_bulk_movies(limit=2000, download_posters=True):
    """
    Загружает limit фильмов из TMDB (popular + now_playing)
    """

    total_saved = 0
    endpoints = ["/movie/top_rated"]

    for endpoint in endpoints:
        page = 1

        while total_saved < limit:
            data = tmdb_request(endpoint, {"page": page})
            results = data.get("results", [])

            if not results:
                break

            for movie_data in results:
                if total_saved >= limit:
                    break

                detail_data = get_movie_detail(movie_data["id"])
                movie = save_movie_from_tmdb(detail_data)

                if download_posters:
                    download_and_save_poster(movie)

                total_saved += 1
                print(f"Сохранено: {total_saved}")

            page += 1

            if page > data.get("total_pages", 1):
                break

        if total_saved >= limit:
            break

    print("Импорт завершён")
    return total_saved