# ReelTalk – Project Documentation

## 1. Introduction
ReelTalk is a Django-based online community for movie lovers. Members discover movies, rate and review films, manage watchlists, like reviews and follow other reviewers. Administrators manage movie content, genres and reported reviews.

## 2. Problem Definition
Movie information, ratings, reviews and personal watchlists are often spread across separate services. ReelTalk brings these activities into one responsive web application.

## 3. Objectives
- Provide searchable movie discovery.
- Support member registration and authentication.
- Display posters, genres, cast, director, year and descriptions.
- Allow one rating/review per member per movie.
- Maintain want-to-watch and watched lists.
- Enable follows, review likes and review reports.
- Show trending and top-rated movie collections.
- Provide administration and moderation tools.

## 4. Scope and Users
**Administrator:** manages movies and genres, moderates reports, manages accounts through Django admin and views content.

**Member:** registers, logs in, browses and filters movies, rates/reviews, saves movies, follows reviewers, likes/reports reviews and views profiles.

## 5. Technology Stack
Python 3, Django, HTML5, CSS3, Bootstrap 5, JavaScript (Bootstrap interactions), SQLite3 and Pillow.

## 6. Functional Requirements
1. Registration, login and logout.
2. Movie CRUD for staff.
3. Genre management through Django admin.
4. Search by title, director or cast.
5. Filter by genre and year.
6. Movie detail and poster display.
7. Rating from 1 to 5 and written review.
8. Watchlist and watched status.
9. Follow/unfollow members.
10. Like/unlike reviews.
11. Report reviews and mark reports resolved.
12. Trending and top-rated listings.
13. Member profile and review history.

## 7. Non-Functional Requirements
- Authentication and authorization for protected actions.
- Responsive layout for desktop and mobile.
- Maintainable Django app structure.
- Server-side validation and CSRF protection.
- Consistent database relationships and uniqueness constraints.
- Clear user feedback for successful actions.

## 8. Database Design
- User: Django authentication user.
- Genre: name.
- Movie: title, year, director, cast, poster, description and many-to-many genres.
- Review: user, movie, rating, text and timestamps; one review per user/movie.
- Watchlist: user, movie, status (watchlist/watched); one entry per user/movie.
- Follow: follower and following user; unique pair and no self-follow.
- ReviewLike: user and review; unique pair.
- ReviewReport: reporting user, review, reason, timestamp and resolved flag.

## 9. Relationship Summary
A genre contains many movies; a movie has many reviews; a user writes many reviews; a user saves many movies; users follow other users; reviews receive likes and reports.

## 10. Workflow
Admin creates genres and movies. Members register and search/filter the catalogue. A member saves a movie, changes it to watched after viewing, then submits a rating and review. Other members can like or report reviews and follow reviewers. Home-page rankings update from review count and average rating.

## 11. Testing Plan
- Register with valid and invalid data.
- Login/logout and access control.
- Add/edit/delete movies as staff.
- Upload poster and verify display.
- Search and filter movies.
- Submit and update a rating/review.
- Verify duplicate review prevention.
- Add/update watchlist status.
- Follow/unfollow and prevent self-follow.
- Like/unlike and prevent duplicate likes.
- Submit and resolve a review report.
- Verify trending and top-rated ordering.
- Check pages at desktop and mobile widths.

## 12. Limitations and Future Enhancements
Potential future work: email verification and password reset via configured email, pagination, AJAX interactions, user avatars, notifications, advanced recommendation algorithms, automated tests, deployment, and stronger moderation workflows.

## 13. Conclusion
ReelTalk combines movie discovery, ratings, reviews and social features in a single Django application. The modular data model and Django authentication/admin provide a foundation for future development and deployment.
