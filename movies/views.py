from django.shortcuts import render
from django.views.generic import TemplateView
import requests

import re
from django.contrib.postgres.search import TrigramSimilarity

import traceback

from .models import Movie
from .services.tmdb import search_movie, get_movie_detail
from .services.movie_service import save_movie_from_tmdb


class HomeView(TemplateView):
    template_name = "movies/home_page.html"

    def get(self, request, *args, **kwargs):

        query = request.GET.get("q")

        hero_movie = None
        similar_movies = None
        popular_movies = None
        top_movies = None
        new_movies = None
        error = None


        # ГЛАВНАЯ БЕЗ ПОИСКА
        if not query:
            popular_movies = Movie.objects.order_by("-popularity")[:20]
            top_movies = Movie.objects.order_by("-vote_average")[:20]
            new_movies = Movie.objects.order_by("-release_date")[:20]
            hero_movie = Movie.objects.order_by("?").first()


        # ПОИСК
        if query:
            year = None
            year_match = re.search(r"(19|20)\d{2}", query)

            if year_match:
                year = int(year_match.group())
                query = query.replace(str(year), "").strip()

            try:
                search_data = search_movie(query)

                if search_data.get("results"):
                    movie_id = search_data["results"][0]["id"]
                    detail_data = get_movie_detail(movie_id)
                    hero_movie = save_movie_from_tmdb(detail_data)

                elif not search_data.get("results"):
                    hero_movie = Movie.objects.order_by("?").first()
                else:
                    error = "Фильм не найден"
                hero_movie = hero_movie

            except Exception as e:
                print("TMDB ERROR:", e)
                traceback.print_exc()

            queryset = Movie.objects.annotate(
                similarity=TrigramSimilarity("title", query)
            ).filter(similarity__gt=0.3)

            if year:
                queryset = queryset.filter(release_date__year=year)

            if hero_movie:
                similar_movies = queryset.exclude(id=hero_movie.id).order_by("-similarity")[:20]
            else:
                similar_movies = queryset.order_by("-similarity")[:20]

        return render(request, self.template_name, {

            "hero_movie": hero_movie,
            "query": bool(query),
            "similar_movies": similar_movies,
            "popular_movies": popular_movies,
            "top_movies": top_movies,
            "new_movies": new_movies,
            "error": error,
        })


class MovieDetailView(TemplateView):
    template_name = "movies/movie_detail.html"
    model = Movie
    context_object_name = "movie"

    def get(self, request, *args, **kwargs):
        ...