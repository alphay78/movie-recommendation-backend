from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Movie API",
        default_version="v1",
        description="Movie Recommendation Backend API",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # users
    path('api/auth/', include('users.urls')),
    
    # movies
    path('api/movies/', include('movies.urls')),

    # swagger docs
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-ui"),
]
