from django.db import transaction
from django.core.cache import cache
from django.conf import settings

from rest_framework import generics, status, permissions, filters, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Favorite
from .serializers import MovieSerializer, FavoriteSerializer
from .services import (
    fetch_trending_movies,
    fetch_movie_details,
    tmdb_get,
    TMDbError,
)

CACHE_TTL = getattr(settings, "TMDB_CACHE_TTL", 60 * 60)  # 1 hour
RECOMMENDATION_LIMIT = 20


# ---------------------------------------------------------
# Pagination
# ---------------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50


# ---------------------------------------------------------
# 1. MOVIE LIST + FILTERS + SEARCH
# ---------------------------------------------------------
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "release_date"]
    search_fields = ["title", "overview"]
    ordering_fields = ["popularity", "release_date", "title"]
    ordering = ["-popularity"]


# ---------------------------------------------------------
# 2. MOVIE DETAIL
# ---------------------------------------------------------
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"


# ---------------------------------------------------------
# 3. TRENDING MOVIES (TMDB)
# ---------------------------------------------------------
class TrendingMoviesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cache_key = "tmdb_trending_week_v2"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        try:
            data = fetch_trending_movies()
        except TMDbError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        results = data.get("results", [])[:20]
        payload = []
        movies_to_upsert = []

        for item in results:
            movie_id = item.get("id")
            title = item.get("title") or item.get("name") or ""
            overview = item.get("overview") or ""
            poster_path = item.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            release_date = item.get("release_date") or item.get("first_air_date")
            popularity = item.get("popularity") or 0

            obj = {
                "movie_id": movie_id,
                "title": title,
                "overview": overview,
                "poster_url": poster_url,
                "release_date": release_date,
                "popularity": popularity,
            }
            payload.append(obj)
            movies_to_upsert.append(obj)

        with transaction.atomic():
            for m in movies_to_upsert:
                Movie.objects.update_or_create(
                    movie_id=m["movie_id"],
                    defaults=m,
                )

        cache.set(cache_key, payload, CACHE_TTL)
        return Response(payload)


# ---------------------------------------------------------
# 4. RECOMMENDATIONS
# ---------------------------------------------------------
class RecommendedMoviesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"recommendations_v2_{user.id}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        favorites = Favorite.objects.filter(user=user).select_related("movie")

        if not favorites.exists():
            try:
                data = fetch_trending_movies()
            except TMDbError as e:
                return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

            results = data.get("results", [])[:RECOMMENDATION_LIMIT]
            payload = [{"movie_id": r.get("id"), "title": r.get("title") or r.get("name")} for r in results]

            cache.set(cache_key, payload, CACHE_TTL)
            return Response(payload)

        recommendations = []
        seen = set()
        favorite_movie_ids = [fav.movie.movie_id for fav in favorites][:5]

        for fav_id in favorite_movie_ids:
            try:
                rec_data = tmdb_get(f"/movie/{fav_id}/recommendations", {"page": 1})
            except TMDbError:
                continue

            for r in rec_data.get("results", [])[:5]:
                mid = r.get("id")
                if not mid or mid in seen:
                    continue
                seen.add(mid)

                recommendations.append({"movie_id": mid, "title": r.get("title") or r.get("name")})

                if len(recommendations) >= RECOMMENDATION_LIMIT:
                    break

            if len(recommendations) >= RECOMMENDATION_LIMIT:
                break

        if not recommendations:
            try:
                data = fetch_trending_movies()
            except TMDbError as e:
                return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

            recommendations = [
                {"movie_id": r.get("id"), "title": r.get("title") or r.get("name")}
                for r in data.get("results", [])[:RECOMMENDATION_LIMIT]
            ]

        cache.set(cache_key, recommendations, CACHE_TTL)
        return Response(recommendations)


# ---------------------------------------------------------
# 5. FAVORITES: List + Create
# ---------------------------------------------------------
class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("movie").order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        movie_id = serializer.validated_data.get("movie_id")

        movie_obj = Movie.objects.filter(movie_id=movie_id).first()
        if not movie_obj:
            raise serializers.ValidationError({"detail": "Movie not found in database."})

        if Favorite.objects.filter(user=user, movie=movie_obj).exists():
            raise serializers.ValidationError({"detail": "Movie already in favorites."})

        serializer.save(user=user, movie=movie_obj)


# ---------------------------------------------------------
# 6. FAVORITES: Delete
# ---------------------------------------------------------
class FavoriteDestroyView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
