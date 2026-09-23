# Music Discovery App

A scalable backend service built with Django that provides music recommendations based on user preferences such as genres, artists, and moods.

The project uses PostgreSQL for persistent data storage, Redis for caching, Celery for background processing, and Docker for containerized deployment.

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Celery Beat
* Docker
* Nginx
* Spotify Web API integration

## Features

* Create and retrieve user profiles
* Store user music preferences
* Store user listening activity
* Generate music recommendations
* Cache recommendations using Redis
* Refresh recommendations asynchronously using Celery
* Periodically refresh recommendations for all users using Celery Beat
* Store recommendations in PostgreSQL
* Analytics APIs for overall and user-level activity
* Dockerized application
* Nginx reverse proxy

## Project Structure

```text
music-discovery/
│
├── activity/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── analytics/
│   ├── views.py
│   └── urls.py
│
├── recommendations/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── spotify.py
│   ├── tasks.py
│   ├── views.py
│   └── urls.py
│
├── users/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
│
├── nginx/
│   └── nginx.conf
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── manage.py
└── README.md
```

## Environment Configuration

Create a `.env` file in the project root.

Example:

```env
DB_NAME=music_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

The actual `.env` file should not be committed to Git.

Use `.env.example` as the configuration template.

## Running the Project with Docker

Make sure Docker Desktop is running.

From the project root:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

The following services should be running:

* PostgreSQL
* Redis
* Django Web
* Celery Worker
* Celery Beat
* Nginx

## Database Migrations

Run migrations using the Django container:

```bash
docker compose exec web python manage.py migrate
```

## API Base URL

Nginx is configured as the reverse proxy.

```text
http://localhost
```

Django can also be accessed directly through:

```text
http://localhost:8000
```

## API Documentation

### 1. Create User

**POST**

```text
/users/
```

Example request:

```json
{
    "name": "Rahul",
    "email": "rahul@example.com",
    "genres": ["pop", "rock"],
    "artists": ["The Weeknd"],
    "moods": ["happy", "energetic"]
}
```

Example response:

```json
{
    "id": 1,
    "name": "Rahul",
    "email": "rahul@example.com",
    "created_at": "2026-09-23T06:33:34.407572Z"
}
```

### 2. Get User

**GET**

```text
/users/{user_id}/
```

Example:

```text
GET /users/1/
```

Returns the user's profile and music preferences.

### 3. Refresh Recommendations

**POST**

```text
/recommendations/{user_id}/refresh/
```

Example:

```text
POST /recommendations/1/refresh/
```

Response:

```json
{
    "message": "Recommendation refresh started"
}
```

The refresh operation is processed asynchronously using Celery.

### 4. Get Recommendations

**GET**

```text
/recommendations/{user_id}/
```

Example:

```text
GET /recommendations/1/
```

Returns recommendations for the specified user.

Recommendations are first checked in Redis. If they are not available in the cache, the application retrieves them from PostgreSQL and stores them in Redis.

### 5. Create User Activity

**POST**

```text
/activity/
```

Example:

```json
{
    "user": 1,
    "spotify_track_id": "dummy001",
    "track_name": "Blinding Lights",
    "artist_name": "The Weeknd",
    "action": "play"
}
```

Supported actions:

* `play`
* `like`
* `skip`

### 6. Analytics Summary

**GET**

```text
/analytics/summary/
```

Returns overall application statistics such as:

* Total users
* Total activities
* Total recommendations
* Total plays
* Total likes
* Total skips

### 7. Analytics Trends

**GET**

```text
/analytics/trends/
```

Returns trending artists and genres based on stored user activity and preferences.

### 8. User Analytics

**GET**

```text
/analytics/user/{user_id}/
```

Example:

```text
GET /analytics/user/1/
```

Returns activity statistics for a specific user.

## Redis Caching

Redis is used as a temporary cache for user recommendations.

Cache key format:

```text
recommendations_user_{user_id}
```

Example:

```text
recommendations_user_1
```

The recommendation cache has a 5-minute expiration time.

When recommendations are refreshed, the existing Redis cache is deleted so that the next request receives the refreshed data.

## Celery

Celery is used to process recommendation refreshes in the background.

When the API receives:

```text
POST /recommendations/1/refresh/
```

the API sends a task to Celery instead of performing the entire operation during the HTTP request.

This keeps the API response fast.

## Celery Beat

Celery Beat is configured to periodically refresh recommendations for all users.

Current schedule:

```text
Every 1 hour
```

Celery Beat triggers:

```text
refresh_all_users_task
```

This task queues recommendation refresh tasks for individual users.

## PostgreSQL

PostgreSQL is used as the main persistent database.

It stores:

* User profiles
* User preferences
* User activities
* Recommendation records

## Nginx

Nginx acts as a reverse proxy in front of the Django application.

Request flow:

```text
Client
   ↓
Nginx :80
   ↓
Django :8000
   ↓
PostgreSQL / Redis
```

## Spotify Integration

The application contains a Spotify integration layer in:

```text
recommendations/spotify.py
```

The application is designed to use the Spotify Web API for retrieving recommendation data based on user preferences.

Currently, the project uses dummy recommendation data because access to the Spotify Web API is not available with the current Spotify account configuration.

The integration can be replaced with the actual Spotify API implementation once valid API access and credentials are available.

## Assumptions

* A user has one preference record.
* User preferences contain genres, artists, and moods.
* Recommendation refreshes are asynchronous.
* Redis is used for temporary recommendation caching.
* PostgreSQL is the persistent data store.
* Celery uses Redis as its broker and result backend.
* Nginx is used as the reverse proxy.
* Recommendation data currently comes from a dummy Spotify integration.

## Limitations

* Real Spotify Web API integration is currently unavailable due to account/API access restrictions.
* Authentication and authorization are not implemented.
* Rate limiting is not implemented.
* Unit tests are not currently included.
* Recommendation logic is currently based on dummy data rather than a production recommendation model.
* Redis caching is currently used for recommendation responses; Spotify raw responses are not stored in a separate database model.

## Useful Docker Commands

Start services:

```bash
docker compose up -d
```

Rebuild and start:

```bash
docker compose up -d --build
```

Stop services:

```bash
docker compose down
```

Check services:

```bash
docker compose ps
```

View Django logs:

```bash
docker compose logs web
```

View Celery logs:

```bash
docker compose logs celery
```

View Celery Beat logs:

```bash
docker compose logs celery-beat
```

Open Redis CLI:

```bash
docker compose exec redis redis-cli
```

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

## Current Architecture

```text
                    ┌──────────────┐
                    │    Client    │
                    │   Postman    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Nginx     │
                    │    :80       │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Django    │
                    │   REST API   │
                    └───┬──────┬───┘
                        │      │
             ┌──────────┘      └──────────┐
             ▼                            ▼
      ┌──────────────┐             ┌──────────────┐
      │ PostgreSQL   │             │    Redis     │
      │ Persistent   │             │    Cache     │
      │   Storage    │             └──────┬───────┘
      └──────────────┘                    │
                                          │
                               ┌──────────┴──────────┐
                               │                     │
                               ▼                     ▼
                        ┌──────────────┐      ┌──────────────┐
                        │ Celery       │      │ Celery Beat  │
                        │ Worker       │      │ Scheduler    │
                        └──────────────┘      └──────────────┘
```

## Project Status

Core backend functionality is implemented and containerized.

Implemented:

* User management
* User preferences
* Activity tracking
* Recommendations
* Redis caching
* Celery background processing
* Celery Beat periodic refresh
* PostgreSQL persistence
* Analytics APIs
* Docker setup
* Nginx reverse proxy

Spotify Web API integration remains pending due to API access restrictions.
