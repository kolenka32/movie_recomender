from django.utils.dateparse import parse_date
from movies.models import Movie, Genre
import requests
from django.core.files.base import ContentFile

#Скачивание фильма из TMDB в локальную бд

def save_movie_from_tmdb(data):

    if not data.get('poster_path') or not data.get('backdrop_path'):
        print('Пропущен (нет постера или фона):', data.get('title') or data.get('name'))
        return None

    if data.get("vote_count", 0) < 50:
        print("Пропущен (слишком мало голосов):", data.get("title") or data.get("name"))
        return None


    movie, created = Movie.objects.update_or_create(
        tmdb_id=data["id"],
        defaults={
            "title": data.get("title") or data.get("name"),
            "original_title": data.get("original_title") or data.get("original_name"),
            "overview": data.get("overview"),

            "release_date": parse_date(
                data.get("release_date") or data.get("first_air_date")
            ) if (data.get("release_date") or data.get("first_air_date")) else None,

            "poster_path": data.get("poster_path"),
            "backdrop_path": data.get("backdrop_path"),

            "vote_average": data.get("vote_average"),
            "vote_count": data.get("vote_count"),
            "popularity": data.get("popularity"),
            "adult": data.get("adult", False),
        }
    )

    print(
        "Создан:", created,
        "| TMDB ID:", data["id"],
        "| name:", data.get("title") or data.get("name"),
    )

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

    if not movie.backdrop_path:
        return

    if movie.local_backdrop:
        return


    poster_url = f"https://image.tmdb.org/t/p/w500{movie.poster_path}"
    backdrop_url = f"https://image.tmdb.org/t/p/original{movie.backdrop_path}"

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

        try:
            response = requests.get(
                backdrop_url,
                proxies=proxies,
                timeout=30
            )
            response.raise_for_status()

            file_name = f"{movie.tmdb_id}_bd.jpg"
            movie.local_backdrop.save(
                file_name,
                ContentFile(response.content),
                save=True
            )
            print("BackDrop сохранён через ImageField")

        except requests.RequestException as e:
            print("Ошибка скачивания:", e)



    except requests.RequestException as e:
        print("Ошибка скачивания:", e)
