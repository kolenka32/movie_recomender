import traceback

from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
import requests

from .models import Movie
from .services.tmdb import search_movie, get_movie_detail
from .services.movie_service import save_movie_from_tmdb, download_and_save_poster
from movies.services.bulk_import_service import fetch_bulk_movies
from django.http import HttpResponse

class HomeView(TemplateView):
    template_name = "movies/home_page.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        movie = None
        error = None

        if query:
            movie = Movie.objects.filter(title__icontains=query).first()

            if not movie:
                try:
                    search_data = search_movie(query)

                    if search_data["results"]:
                        movie_id = search_data["results"][0]["id"]
                        detail_data = get_movie_detail(movie_id)
                        movie = save_movie_from_tmdb(detail_data)

                    else:
                        error = "Фильм не найден"
                        print(error)


                except Exception as e:
                    print("TMDB ERROR:", e)
                    traceback.print_exc()
                    error = str(e)



        print('Запроса нет')
        return render(request, self.template_name, {"movie": movie, "error": error})




def import_movies_view(request):
    total = fetch_bulk_movies(limit=2000)
    return HttpResponse(f"Импортировано фильмов: {total}")