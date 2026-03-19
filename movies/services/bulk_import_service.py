from movies.services.tmdb import tmdb_request, get_movie_detail, get_tv_detail, discover_movies
from movies.services.movie_service import save_movie_from_tmdb, download_and_save_poster


def fetch_bulk_content(limit=4000):

    total_saved = 0

    endpoints = [

        # фильмы
        ("/movie/popular", "movie"),
        ("/movie/top_rated", "movie"),
        ("/movie/now_playing", "movie"),
        ("/movie/upcoming", "movie"),

        # сериалы
        ("/tv/popular", "tv"),
        ("/tv/top_rated", "tv"),
        ("/tv/on_the_air", "tv"),
        ("/tv/airing_today", "tv"),
    ]

    for endpoint, content_type in endpoints:

        page = 1

        while total_saved < limit:

            data = tmdb_request(endpoint, {"page": page})
            results = data.get("results", [])

            if not results:
                break

            for item in results:

                if total_saved >= limit:
                    break

                try:

                    if content_type == "movie":
                        detail = get_movie_detail(item["id"])
                    else:
                        detail = get_tv_detail(item["id"])

                    movie = save_movie_from_tmdb(detail)

                    if not movie:
                        continue

                    download_and_save_poster(movie)

                    total_saved += 1

                    print("Сохранено:", total_saved)

                except Exception as e:
                    print("Ошибка:", e)

            page += 1

            if page > data.get("total_pages", 1):
                break

        if total_saved >= limit:
            break

    print("Импорт завершён")

    return total_saved


def import_mass_movies():

    total_saved = 0
    years = range(2011, 2026) #импорт фильмов по годам

    for year in years:
        print("YEAR:", year)

        for page in range(1, 501):
            data = discover_movies(page=page, year=year)
            results = data.get("results", [])

            if not results:
                break

            for movie_data in results:

                try:
                    detail = get_movie_detail(movie_data["id"])
                    movie = save_movie_from_tmdb(detail)

                    if not movie:
                        continue

                    download_and_save_poster(movie)
                    total_saved += 1

                    if total_saved % 100 == 0:
                        print("Saved:", total_saved)

                except Exception as e:
                    print("Error:", e)

    print("TOTAL SAVED:", total_saved)