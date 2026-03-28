# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, Genre
from django.contrib import admin
from .models import Movie, Genre



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_id", "name")
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "original_title", "release_date", "vote_average", "poster_preview", "backdrop_preview")
    list_filter = ("release_date", "adult", "genres")
    search_fields = ("id", "title", "original_title")
    filter_horizontal = ("genres",)
    readonly_fields = ("tmdb_id", "poster_preview", "backdrop_preview", "release_date",
                       "poster_path", "backdrop_path", "vote_average", "vote_count",
                       "popularity", "adult", "created_at", "updated_at"

                       )

    fieldsets = (
        ("Основное", {
            "fields": ("title", "original_title", "overview", "release_date", "adult")
        }),
        ("TMDB", {
            "fields": (
                "tmdb_id",
                "poster_path",
                "backdrop_path",
                "vote_average",
                "vote_count",
                "popularity",
            )
        }),
        ("Постер", {
            "fields": ("local_poster", "poster_preview", "local_backdrop", "backdrop_preview")
        }),

        ("Жанры", {
            "fields": ("genres",)
        }),
    )

    def poster_preview(self, obj):
        # 1. если есть локальный постер
        if obj.local_poster:
            return format_html(
                '<img src="{}" style="height:90px; border-radius:6px;" />',
                obj.local_poster.url
            )
        # 2. если есть постер с TMDB
        if obj.poster_path:
            return format_html(
                '<img src="{}" style="height:120px; border-radius:6px;" />',
                obj.poster_path
            )
        return "—"

    poster_preview.short_description = "Постер"

    def backdrop_preview(self, obj):
        if obj.local_backdrop:
            return format_html(
                '<img src="{}" style="height:90px; border-radius:6px;" />',
                obj.local_backdrop.url
            )
        if obj.backdrop_path:
            return format_html(
                '<img src="{}" style="height:120px; border-radius:6px;" />',
                obj.backdrop_path
            )
        return '—'

    backdrop_preview.short_description = "Фон"