import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel

class BaseModel(models.Model):
    """
    Base Model with UUID Primary Key and Timestamped Models which provides created
    and modified functionalities.
    Will be used globally by all Apps as standard accross the Project.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
