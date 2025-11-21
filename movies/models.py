from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)  # TMDb ID
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    release_date = models.CharField(max_length=20, blank=True, null=True)
    popularity = models.FloatField(default=0)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # prevents duplicates

    def __str__(self):
        return f"{self.user.username} -> {self.movie.title}"
