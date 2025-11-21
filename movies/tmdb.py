import os
import requests
from requests.exceptions import RequestException
from django.conf import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Load API key from settings or environment
TMDB_API_KEY = getattr(settings, "TMDB_API_KEY", os.getenv("TMDB_API_KEY"))


class TMDbError(Exception):
    """Custom error for TMDb failures."""
    pass


def tmdb_get(path, params=None):
    """Generic GET request to TMDb API with error handling."""
    if params is None:
        params = {}

    params["api_key"] = TMDB_API_KEY
    params["language"] = "en-US"

    url = f"{TMDB_BASE_URL}{path}"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        raise TMDbError(f"TMDb request failed: {e}")

    return response.json()


def fetch_trending_movies(media_type="movie", time_window="week", page=1):
    """Get trending movies from TMDb."""
    path = f"/trending/{media_type}/{time_window}"
    return tmdb_get(path, {"page": page})


def fetch_movie_details(tmdb_id):
    """Get full movie details."""
    path = f"/movie/{tmdb_id}"
    return tmdb_get(path)
