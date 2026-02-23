from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
import requests
from googletrans import Translator  # pip install googletrans==4.0.0-rc1

API_KEY = settings.OMDB_API_KEY

class HomeView(TemplateView):
    template_name = "movies/home_page.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        movie = None
        error = None

        if query:
            # Переводим с русского на английский
            translator = Translator()
            translated = translator.translate(query, src='ru', dest='en').text

            url = "https://www.omdbapi.com/"
            params = {
                "apikey": API_KEY,
                "t": translated,  # поиск на английском
                "plot": "full",
                "r": "json"
            }

            response = requests.get(url, params=params)
            data = response.json()

            if data.get("Response") == "True":
                movie = data
            else:
                error = data.get("Error")

        return render(request, self.template_name, {
            "movie": movie,
            "error": error
        })