from code import interact

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.contrib.postgres.search import TrigramSimilarity


import requests
from datetime import date
import random
import re
import traceback

from .models import Movie
from .services.tmdb import search_movie, get_movie_detail
from .services.movie_service import save_movie_from_tmdb, get_recommendation_for_user
from .services.search import smart_search

from users.models import UserMovieInteraction



class HomeView(TemplateView):
    template_name = "movies/home_page.html"

    def get(self, request, *args, **kwargs):

        query = request.GET.get("q")
        context = {
            "title": 'Главная',
        }

        if query:
            try:
                movies = smart_search(query)

                hero_movie = movies[0] if movies else None

                context.update({
                    'query': query,
                    'hero_movie': hero_movie,
                    'similar_movies': movies[1:],
                })

            except Exception as e:
                context['error'] = str(e)

        else:
            popular_movies = Movie.objects.order_by("-popularity")[:20]
            top_movies = Movie.objects.order_by("-vote_average")[:20]
            new_movies = Movie.objects.order_by("-release_date")[:20]

            hero_movie = random.choice(popular_movies) and random.choice(top_movies) and random.choice(new_movies) if popular_movies and top_movies and new_movies else None

            context.update({
                "popular_movies": popular_movies,
                "top_movies": top_movies,
                "new_movies": new_movies,
                "hero_movie": hero_movie,
            })

            if request.user.is_authenticated:
                interactions = UserMovieInteraction.objects.filter(user=request.user)
                favorite_genres = request.user.favorite_genres.all()
                watched_movies_ids = interactions.filter(
                    Q(is_watched=True) | Q(is_liked=True)
                    ).values_list('movie_id', flat=True)

                genre_recommendations = Movie.objects.filter(
                    genres__in = favorite_genres
                ).exclude(id__in = watched_movies_ids).distinct()

                try:
                    ai_recommendations = get_recommendation_for_user(request.user)
                except:
                    ai_recommendations = Movie.objects.none()

                recommendations = (
                    genre_recommendations.union(ai_recommendations).order_by(
                        "-popularity")[:20]
                )

                context["recommended_movies"] = recommendations

        return TemplateResponse(request, self.template_name, context)


class MovieDetailView(TemplateView):
    template_name = "movies/movie_detail.html"

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get("movie_id")

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            movie = None

        interaction = None

        if request.user.is_authenticated and movie:
            interaction = UserMovieInteraction.objects.filter(
                user=request.user,
                movie=movie
            ).first()

        return TemplateResponse(request, self.template_name, {
            "movie": movie,
            "interaction": interaction
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return TemplateResponse(request, "components/auth_required.html", {})

        movie_id = kwargs.get("movie_id")
        action = request.POST.get("action")

        movie = Movie.objects.get(id=movie_id)

        interaction, _ = UserMovieInteraction.objects.get_or_create(
            user=request.user,
            movie=movie
        )

        if action == "watched":
            interaction.is_watched = not interaction.is_watched

        elif action == "favorite":
            interaction.is_favorite = not interaction.is_favorite

        elif action == "liked":
            interaction.is_liked = not interaction.is_liked

        interaction.save()

        html = render_to_string(
            "components/movie_actions.html",
            {
                "interaction": interaction,
                "movie": movie,
                "user": request.user
            },
            request=request
        )

        return HttpResponse(html)