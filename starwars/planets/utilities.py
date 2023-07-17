from base.constants import BASE_URL

from planets.models import Planet
from planets.serializers import PlanetSerializer


def save_planets():
    """
    Fetches and saves movies from the Star Wars API to the database.
    """
    planets_url = f"{BASE_URL}/planets/"
    from base.utilities import save_objects
    # Resolved a Circular Import due to the management command use case.
    save_objects(planets_url, Planet, PlanetSerializer)
