from django.db import models
from base.models import BaseModel
from favorites.models import Favorite
from django.contrib.contenttypes.fields import GenericRelation

class Planet(BaseModel):
    """
    Model Which will store data for all Star Wars Planets, Name is the unique constraint.
    """
    name = models.CharField(max_length=255, unique=True)  # Name of the Movie
    diameter = models.CharField(max_length=255)
    rotation_period = models.CharField(max_length=255)
    orbital_period = models.CharField(max_length=255)
    gravity =models.CharField(max_length=255)
    population = models.CharField(max_length=255)
    climate = models.CharField(max_length=255) # The opening paragraphs at the beginning of this film.
    favorite = GenericRelation(Favorite)
    #  Following Fields are commented right now and not mapped to minimize the Scope of this Assignment
    # climate string -- The climate of this planet. Comma separated if diverse.
    # terrain string -- The terrain of this planet. Comma separated if diverse.
    # surface_water string -- The percentage of the planet surface that is naturally occurring water or bodies of water.
    # residents array -- An array of People URL Resources that live on this planet.
    # films array -- An array of Film URL Resources that this planet has appeared in.
    # url string -- the hypermedia URL of this resource.
    # created string -- the ISO 8601 date format of the time that this resource was created.
    # edited string -- the ISO 8601 date format of the time that this resource was edited.
    def __str__(self):
        return self.name
