from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

class Favorite(models.Model):
    """
    Used a Generic Foreign Key as this can support both favorite Movie as well
      as Planet and can be scaled to automatically support Characters etc
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(default=uuid.uuid4)
    content_object = GenericForeignKey('content_type', 'object_id')
    custom_name = models.CharField(max_length=255, blank=True, default="")
    user_identifier = models.UUIDField(default=uuid.uuid4)