from django.utils.dateparse import parse_date
from movies.models import Movie, Genre
from django.utils import timezone
import os
import requests
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile

def save_movie_from_tmdb(data):
    movie, created = Movie.objects.update_or_create(
        tmdb_id=data["id"],
        defaults={
            "title": data["title"],
            "original_title": data.get("original_title"),
            "overview": data.get("overview"),
            "release_date": parse_date(data.get("release_date")) if data.get("release_date") else None,
            "poster_path": data.get("poster_path"),
            "backdrop_path": data.get("backdrop_path"),
            "vote_average": data.get("vote_average"),
            "vote_count": data.get("vote_count"),
            "popularity": data.get("popularity"),
            "adult": data.get("adult", False),
        }
    )
    print("Создан новый фильм:", created, "| TMDB ID:", data["id"])
    movie.genres.clear()

    for genre_data in data.get("genres", []):
        genre, _ = Genre.objects.get_or_create(
            tmdb_id=genre_data["id"],
            defaults={"name": genre_data["name"]}
        )
        movie.genres.add(genre)


    return movie



def download_and_save_poster(movie):

    if not movie.poster_path:
        return

    if movie.local_poster:
        return

    poster_url = f"https://image.tmdb.org/t/p/w500{movie.poster_path}"

    proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }

    try:
        response = requests.get(
            poster_url,
            proxies=proxies,
            timeout=30
        )
        response.raise_for_status()

        file_name = f"{movie.tmdb_id}.jpg"

        movie.local_poster.save(
            file_name,
            ContentFile(response.content),
            save=True
        )

        print("Постер сохранён через ImageField")

    except requests.RequestException as e:
        print("Ошибка скачивания:", e)



def download_image_with_tor_proxy(url, output_path):

    proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }

    try:
        # Скачивание изображения
        response = requests.get(
            url,
            proxies=proxies,
            stream=True,
            timeout=30
        )
        response.raise_for_status()

        # Проверка, что это действительно изображение
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            print(f"Предупреждение: URL может не быть изображением (Content-Type: {content_type})")

        # Сохранение файла
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Изображение успешно скачано: {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании: {e}")
        return False
