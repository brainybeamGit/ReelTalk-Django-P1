from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Genre, Movie, Review, Watchlist, Follow, ReviewLike

class ReelTalkTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="filmfan", password="Testpass123!")
        self.other = User.objects.create_user(username="critic", password="Testpass123!")
        self.genre = Genre.objects.create(name="Drama")
        self.movie = Movie.objects.create(title="Sample Film", year=2024, director="A Director", description="A sample movie")
        self.movie.genres.add(self.genre)

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Film")

    def test_member_can_register(self):
        response = self.client.post(reverse("register"), {
            "username": "newmember", "email": "new@example.com",
            "password1": "VeryStrongPass123!", "password2": "VeryStrongPass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newmember").exists())

    def test_member_can_review_movie(self):
        self.client.login(username="filmfan", password="Testpass123!")
        response = self.client.post(reverse("add_review", args=[self.movie.pk]), {"rating": 5, "text": "Excellent film"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, movie=self.movie, rating=5).exists())

    def test_member_can_add_to_watchlist(self):
        self.client.login(username="filmfan", password="Testpass123!")
        self.client.post(reverse("set_watch_status", args=[self.movie.pk, "watchlist"]))
        self.assertTrue(Watchlist.objects.filter(user=self.user, movie=self.movie, status="watchlist").exists())

    def test_member_can_follow_another_member(self):
        self.client.login(username="filmfan", password="Testpass123!")
        self.client.post(reverse("toggle_follow", args=[self.other.username]))
        self.assertTrue(Follow.objects.filter(follower=self.user, following=self.other).exists())

    def test_average_rating_is_calculated(self):
        Review.objects.create(user=self.user, movie=self.movie, rating=4, text="Good")
        self.assertEqual(self.movie.average_rating, 4)
