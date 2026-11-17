from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("movie/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("movie/<int:pk>/list/<str:status>/", views.set_watch_status, name="set_watch_status"),
    path("movie/<int:pk>/review/", views.add_review, name="add_review"),
    path("review/<int:pk>/like/", views.like_review, name="like_review"),
    path("review/<int:pk>/report/", views.report_review, name="report_review"),
    path("search/", views.home, name="search"),
    path("watchlist/", views.my_list, name="my_list"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
    path("manage/movies/", views.manage_movies, name="manage_movies"),
    path("manage/movies/add/", views.movie_create, name="movie_create"),
    path("manage/movies/<int:pk>/edit/", views.movie_edit, name="movie_edit"),
    path("manage/movies/<int:pk>/delete/", views.movie_delete, name="movie_delete"),
    path("manage/reports/", views.manage_reports, name="manage_reports"),
]
