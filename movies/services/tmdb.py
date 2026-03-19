import requests
import time
from django.conf import settings

#Запрос к TMDB через прокси тор браузера

PROXIES = {
    "http": "socks5h://127.0.0.1:9150",
    "https": "socks5h://127.0.0.1:9150",
}


def tmdb_request(endpoint, params=None, retries=5):
    base_url = "https://api.themoviedb.org/3"
    url = f"{base_url}{endpoint}"

    default_params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU",
    }

    if params:
        default_params.update(params)

    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                params=default_params,
                proxies=PROXIES,
                timeout=60,
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"TMDB retry {attempt+1}/{retries}: {e}")
            time.sleep(3)

    raise Exception("TMDB request failed after retries")




def search_movie(query, extra_params=None):
    params = {"query": query}
    if extra_params:
        params.update(extra_params)

    return tmdb_request("/search/multi", params)


def get_movie_detail(movie_id):
    return tmdb_request(f"/movie/{movie_id}")


def get_tv_detail(tv_id):
    return tmdb_request(f"/tv/{tv_id}")


def discover_movies(page=1, year=None):

    params = {
        "page": page,
        "sort_by": "popularity.desc",
        "vote_count.gte": 50,
    }

    if year:
        params["primary_release_year"] = year

    return tmdb_request("/discover/movie", params)