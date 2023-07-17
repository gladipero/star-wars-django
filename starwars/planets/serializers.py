from rest_framework import serializers
from favorites.models import Favorite
from django.contrib.contenttypes.models import ContentType

from planets.models import Planet
from base.constants import DATE_TIME_FORMAT


class PlanetSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format=DATE_TIME_FORMAT, read_only=True)
    updated = serializers.DateTimeField(format=DATE_TIME_FORMAT, read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Planet
        fields = ['id', "is_favorite", "updated", "created", "name", "population", "diameter",
                   "rotation_period", "orbital_period", "gravity", "climate"]

    def get_is_favorite(self, obj):
        user_id = self.context.get('user_id')
        content_type=ContentType.objects.get_for_model(Planet)
        return Favorite.objects.filter(user_id=user_id, object_id=obj.pk, content_type=content_type).exists()
    
class PlanetListSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Planet
        fields = ['id', "is_favorite", "updated", "created", "name", "population", "diameter",
                   "rotation_period", "orbital_period", "gravity", "climate"]

    def get_is_favorite(self, obj):
        user_id = self.context.get('user_id')
        content_type=ContentType.objects.get_for_model(Planet)
        return Favorite.objects.filter(user_id=user_id, object_id=obj.pk, content_type=content_type).exists()
    
    def get_name(self, obj):
        user_id = self.context.get('user_id')
        content_type=ContentType.objects.get_for_model(Planet)
        favorite_obj = Favorite.objects.filter(user_id=user_id, object_id=obj.pk, content_type=content_type).first()
        # If Custom Name is there, will respond with that, else Name is returned.
        if favorite_obj and favorite_obj.custom_name:
            return favorite_obj.custom_name
        return obj.name
