import os
import requests
from requests.exceptions import RequestException
from django.conf import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Load API key from Django settings or environment
TMDB_API_KEY = getattr(settings, "TMDB_API_KEY", os.getenv("TMDB_API_KEY"))


class TMDbError(Exception):
    """Custom exception for TMDb API errors."""
    pass


def tmdb_get(path, params=None):
    """
    Generic GET request to TMDb API with safe exception handling.
    """
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
    """
    Fetch trending movies from TMDb.
    Example: trending/movie/week
    """
    path = f"/trending/{media_type}/{time_window}"
    return tmdb_get(path, {"page": page})


def fetch_movie_details(tmdb_id):
    """
    Fetch single movie detail by TMDb ID.
    """
    path = f"/movie/{tmdb_id}"
    return tmdb_get(path)
