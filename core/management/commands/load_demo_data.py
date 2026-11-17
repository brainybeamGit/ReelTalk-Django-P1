from django.core.management.base import BaseCommand
from core.models import Genre, Movie

class Command(BaseCommand):
    help = "Load sample genres and fictional demo movies into ReelTalk."

    def handle(self, *args, **options):
        genre_names = ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Romance"]
        genres = {name: Genre.objects.get_or_create(name=name)[0] for name in genre_names}
        films = [
            ("The Last Signal", 2024, "Mira Shah", "A radio operator receives a mysterious message.", ["Sci-Fi", "Thriller"]),
            ("Monsoon Letters", 2023, "Arjun Mehta", "Two old friends reconnect through handwritten letters.", ["Drama", "Romance"]),
            ("Midnight Chase", 2025, "Neel Rao", "A detective races across the city to stop a heist.", ["Action", "Thriller"]),
            ("Room for Laughter", 2022, "Tara Joshi", "A family learns to laugh through a chaotic week.", ["Comedy", "Drama"]),
            ("Orbit Seven", 2024, "Kabir Sen", "A small crew investigates an abandoned space station.", ["Sci-Fi", "Action"]),
            ("The Quiet Promise", 2021, "Riya Desai", "A heartfelt story about trust and second chances.", ["Romance", "Drama"]),
            ("Paper City", 2025, "Dev Malhotra", "A journalist uncovers secrets hidden in city archives.", ["Thriller", "Drama"]),
            ("Weekend Trouble", 2023, "Anaya Patel", "A simple holiday becomes a comic adventure.", ["Comedy", "Romance"]),
        ]
        created = 0
        for title, year, director, description, names in films:
            movie, was_created = Movie.objects.get_or_create(
                title=title,
                defaults={"year": year, "director": director, "description": description, "cast": "Demo cast"},
            )
            movie.genres.set([genres[name] for name in names])
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Demo data ready. {created} movies created; {len(genres)} genres available."))
