# ReelTalk – Movie Review and Watchlist Community

Django movie community MVP built with Python, Django, Bootstrap 5, SQLite3 and Pillow.

## Features
- Member registration, login and logout
- Movie catalogue with title/director/cast search and genre/year filters
- Movie posters, genres and details
- One review per member per movie, with 1–5 star rating
- Watchlist and watched status
- Follow/unfollow reviewers
- Like/unlike reviews and report reviews
- Staff movie management and report moderation
- Trending (review count then average rating) and top-rated sections
- Django admin for users, genres and all records

## Setup (Windows PowerShell)
```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Important
- Admin site: http://127.0.0.1:8000/django-admin/
- Staff movie management: log in with a staff account and open `/manage/movies/`.
- Create genres in Django admin before adding movies.
- Uploaded posters are stored in `media/posters/`.
- This starter is for local development/demo. Before public deployment, set `DEBUG=False`, use a secure environment-based `SECRET_KEY`, configure `ALLOWED_HOSTS`, HTTPS, static/media hosting and production database.

## GitHub
```powershell
git add .
git commit -m "Build ReelTalk Django movie community"
git push origin main
```
If your default branch is not `main`, check it with `git branch`.
