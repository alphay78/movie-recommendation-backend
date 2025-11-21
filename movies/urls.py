from django.urls import path
from . import views

urlpatterns = [
    # Trending (TMDB)
    path("trending/", views.TrendingMoviesView.as_view(), name="trending-movies"),

    # Search
    path("search/", views.MovieListView.as_view(), name="search-movies"),

    # Recommendations
    path("recommendations/", views.RecommendedMoviesView.as_view(), name="recommendations"),

    # Favorites
    path("favorites/", views.FavoriteListCreateView.as_view(), name="favorites-list-create"),
    path("favorites/<int:pk>/", views.FavoriteDestroyView.as_view(), name="favorites-destroy"),
]
