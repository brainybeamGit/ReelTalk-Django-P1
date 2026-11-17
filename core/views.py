from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, ReviewForm, MovieForm
from .models import Movie, Genre, Review, Watchlist, Follow, ReviewLike, ReviewReport

def home(request):
    movies = Movie.objects.prefetch_related("genres").annotate(avg_rating=Avg("reviews__rating"), total_reviews=Count("reviews", distinct=True))
    q = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "")
    year = request.GET.get("year", "")
    if q: movies = movies.filter(Q(title__icontains=q) | Q(director__icontains=q) | Q(cast__icontains=q))
    if genre: movies = movies.filter(genres__id=genre)
    if year: movies = movies.filter(year=year)
    context = {
        "movies": movies.order_by("-created_at"),
        "trending": movies.order_by("-total_reviews", "-avg_rating")[:6],
        "top_rated": movies.filter(total_reviews__gt=0).order_by("-avg_rating", "-total_reviews")[:6],
        "genres": Genre.objects.all(),
        "years": Movie.objects.order_by("-year").values_list("year", flat=True).distinct(),
        "query": q,
    }
    return render(request, "core/home.html", context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else: form = RegisterForm()
    return render(request, "core/form.html", {"form": form, "heading": "Create your ReelTalk account"})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.prefetch_related("genres"), pk=pk)
    user_review = Review.objects.filter(movie=movie, user=request.user).first() if request.user.is_authenticated else None
    saved = Watchlist.objects.filter(movie=movie, user=request.user).first() if request.user.is_authenticated else None
    review_form = ReviewForm(instance=user_review)
    return render(request, "core/movie_detail.html", {"movie": movie, "review_form": review_form, "user_review": user_review, "saved": saved})

@login_required
@require_POST
def set_watch_status(request, pk, status):
    if status not in [Watchlist.WATCHLIST, Watchlist.WATCHED]: return redirect("movie_detail", pk=pk)
    movie = get_object_or_404(Movie, pk=pk)
    Watchlist.objects.update_or_create(user=request.user, movie=movie, defaults={"status": status})
    messages.success(request, "Your movie list was updated.")
    return redirect("movie_detail", pk=pk)

@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(user=request.user, movie=movie, defaults=form.cleaned_data)
            messages.success(request, "Your review has been saved.")
    return redirect("movie_detail", pk=pk)

@login_required
@require_POST
def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
    if not created: like.delete()
    return redirect("movie_detail", pk=review.movie_id)

@login_required
@require_POST
def report_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()[:250]
        if reason: ReviewReport.objects.get_or_create(user=request.user, review=review, defaults={"reason": reason})
    return redirect("movie_detail", pk=review.movie_id)

@login_required
def my_list(request):
    entries = Watchlist.objects.filter(user=request.user).select_related("movie").order_by("-added_at")
    return render(request, "core/my_list.html", {"entries": entries})

def profile(request, username):
    person = get_object_or_404(User, username=username)
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=person).exists()
    return render(request, "core/profile.html", {"person": person, "is_following": is_following,
        "reviews": Review.objects.filter(user=person).select_related("movie"),
        "followers": person.followers.count(), "following_count": person.following.count()})

@login_required
@require_POST
def toggle_follow(request, username):
    person = get_object_or_404(User, username=username)
    if person != request.user:
        obj, created = Follow.objects.get_or_create(follower=request.user, following=person)
        if not created: obj.delete()
    return redirect("profile", username=username)

def staff_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)

@staff_required
def manage_movies(request):
    return render(request, "core/manage_movies.html", {"movies": Movie.objects.all()})

@staff_required
def movie_create(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid(): form.save(); messages.success(request, "Movie added."); return redirect("manage_movies")
    return render(request, "core/form.html", {"form": form, "heading": "Add movie"})

@staff_required
def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    if request.method == "POST" and form.is_valid(): form.save(); messages.success(request, "Movie updated."); return redirect("manage_movies")
    return render(request, "core/form.html", {"form": form, "heading": "Edit movie"})

@staff_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST": movie.delete(); messages.success(request, "Movie deleted."); return redirect("manage_movies")
    return render(request, "core/confirm_delete.html", {"object": movie})

@staff_required
def manage_reports(request):
    reports = ReviewReport.objects.select_related("user", "review", "review__movie").order_by("-created_at")
    if request.method == "POST":
        report = get_object_or_404(ReviewReport, pk=request.POST.get("report_id"))
        report.resolved = True
        report.save()
        return redirect("manage_reports")
    return render(request, "core/manage_reports.html", {"reports": reports})
