from django.db import models
from base.models import BaseModel

class Movie(BaseModel):
    """
    Model Which will store data for all Star Wars Movies, Title is the unique constraint.
    """
    title = models.CharField(max_length=255, unique=True)  # Name of the Movie
    release_date = models.DateField()
    director = models.CharField(max_length=100) # Stored as a string with 100 as random length for longer full names
    episode_id = models.IntegerField(null=True) #Null added to handle data inconsistencies from source
    opening_crawl = models.TextField() # The opening paragraphs at the beginning of this film.

    #  Following Fields are commented right now and not mapped to minimize the Scope for First Draft.
    #  Producers string -- The name(s) of the producer(s) of this film. Comma separated.
    #  Species array -- An array of species resource URLs that are in this film.
    #  starships array -- An array of starship resource URLs that are in this film.
    #  vehicles array -- An array of vehicle resource URLs that are in this film.
    #  characters array -- An array of people resource URLs that are in this film.
    def __str__(self):
        return self.title
