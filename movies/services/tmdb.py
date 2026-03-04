import requests
from django.conf import settings


PROXIES = {
    "http": "socks5h://127.0.0.1:9150",
    "https": "socks5h://127.0.0.1:9150",
}


def tmdb_request(endpoint, params=None):
    base_url = "https://api.themoviedb.org/3"
    url = f"{base_url}{endpoint}"

    default_params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU",
    }

    if params:
        default_params.update(params)

    response = requests.get(
        url,
        params=default_params,
        proxies=PROXIES,
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


def search_movie(query):
    return tmdb_request("/search/movie", {"query": query})


def get_movie_detail(movie_id):
    return tmdb_request(f"/movie/{movie_id}")