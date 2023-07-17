from django.urls import path

from planets.views import PlanetListAPIView

urlpatterns = [
    path('', PlanetListAPIView.as_view(), name='planet-list'),
]