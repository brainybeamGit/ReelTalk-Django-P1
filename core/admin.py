from django.contrib import admin
from .models import Genre, Movie, Review, Watchlist, Follow, ReviewLike, ReviewReport
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "director")
    search_fields = ("title", "director")
    list_filter = ("year", "genres")
admin.site.register([Genre, Review, Watchlist, Follow, ReviewLike, ReviewReport])
