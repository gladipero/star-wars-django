from django.urls import path
from movies.views import MovieListAPIView

urlpatterns = [
    path('', MovieListAPIView.as_view(), name='movie-list'),
]