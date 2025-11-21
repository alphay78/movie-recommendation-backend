from rest_framework import serializers
from .models import Movie, Favorite
from .services import fetch_movie_details


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "movie_id", "title", "overview", "poster_url", "release_date", "popularity")


class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "user", "movie", "movie_id", "created_at")
        read_only_fields = ("id", "user", "movie", "created_at")

    def create(self, validated_data):
        user = self.context["request"].user
        tmdb_id = validated_data["movie_id"]

        # Fetch movie details from TMDB API
        tmdb_data = fetch_movie_details(tmdb_id)

        # Create or update Movie model
        movie, _ = Movie.objects.update_or_create(
            movie_id=tmdb_id,
            defaults={
                "title": tmdb_data.get("title", ""),
                "overview": tmdb_data.get("overview", ""),
                "poster_url": f"https://image.tmdb.org/t/p/w500{tmdb_data.get('poster_path')}"
                    if tmdb_data.get("poster_path") else "",
                "release_date": tmdb_data.get("release_date", None),
                "popularity": tmdb_data.get("popularity", 0.0),
            }
        )

        # Create favorite (if already exists, return it)
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            movie=movie
        )

        return favorite
