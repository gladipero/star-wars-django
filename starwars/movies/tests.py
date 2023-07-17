# In the tests.py file

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from movies.models import Movie
from movies.serializers import MovieSerializer

@pytest.mark.django_db
def test_movie_list_api_view():
    # Create some test movie objects
    movie1 = Movie.objects.create(title="Movie 1", release_date="2023-01-01")
    movie2 = Movie.objects.create(title="Movie 2", release_date="2023-02-01")

    # Initialize the API client
    client = APIClient()

    # Get the URL for the Movie List API View
    url = reverse('movie-list')

    # Send a GET request to the API endpoint
    response = client.get(url)

    # Ensure the response status code is 200 OK
    assert response.status_code == 200

