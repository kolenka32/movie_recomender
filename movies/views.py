from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity

import requests
from datetime import date
import random
import re
import traceback

from .models import Movie
from .services.tmdb import search_movie, get_movie_detail
from .services.movie_service import save_movie_from_tmdb, get_recommendation_for_user


class HomeView(TemplateView):
    template_name = "movies/home_page.html"

    def get(self, request, *args, **kwargs):

        query = request.POST.get("q")

        if query:
            ...

        else:
            ...

        return TemplateResponse(request, self.template_name,{
            'title': 'ГЛАВНАЯ'
        })





class MovieDetailView(TemplateView):
    template_name = "movies/movie_detail.html"
    model = Movie
    context_object_name = "movie"

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get("movie_id")

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            movie = None

        return TemplateResponse(request, self.template_name, {
            "movie": movie,
        })