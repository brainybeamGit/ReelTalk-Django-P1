from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self): return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    director = models.CharField(max_length=150)
    cast = models.TextField(blank=True)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
    @property
    def average_rating(self):
        value = self.reviews.aggregate(models.Avg("rating"))["rating__avg"]
        return round(value, 1) if value else 0
    @property
    def review_count(self): return self.reviews.count()

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["user", "movie"], name="one_review_per_user_movie")]
    def __str__(self): return f"{self.user} - {self.movie}"

class Watchlist(models.Model):
    WATCHLIST = "watchlist"
    WATCHED = "watched"
    STATUS_CHOICES = [(WATCHLIST, "Want to watch"), (WATCHED, "Watched")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movie_lists")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="saved_by")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=WATCHLIST)
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "movie"], name="one_list_entry_per_user_movie")]

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="unique_follow"),
            models.CheckConstraint(condition=~models.Q(follower=models.F("following")), name="prevent_self_follow"),
        ]

class ReviewLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "review"], name="unique_review_like")]

class ReviewReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "review"], name="unique_review_reporter_per_review")]
