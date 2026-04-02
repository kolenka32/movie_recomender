from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserMovieInteraction





@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Preferences", {
            "fields": ("favorite_genres",),
        }),
    )

    filter_horizontal = ("groups", "user_permissions", "favorite_genres")


@admin.register(UserMovieInteraction)
class UserMovieInteractionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "is_liked", "is_favorite", "created_at", "updated_at")
    list_filter = ("is_liked", "is_favorite", "created_at", "updated_at")
    search_fields = ("user__username", "movie__title")

    autocomplete_fields = ("user", "movie")

    ordering = ("-created_at",)


class UserMovieInteractionInline(admin.TabularInline):
    model = UserMovieInteraction
    extra = 0
    autocomplete_fields = ("movie",)
