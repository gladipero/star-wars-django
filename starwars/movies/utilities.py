from base.constants import BASE_URL

from movies.models import Movie
from movies.serializers import MovieSerializer


def save_movies():
    """
    Fetches and saves movies from the Star Wars API to the database.
    """
    movies_url = f"{BASE_URL}/films/"
    from base.utilities import save_objects
    # Resolved a Circular Import due to the management command use case.
    save_objects(movies_url, Movie, MovieSerializer)
