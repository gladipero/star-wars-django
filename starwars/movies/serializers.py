from rest_framework import serializers
from movies.models import Movie
from favorites.models import Favorite
from django.contrib.contenttypes.models import ContentType
from base.constants import DATE_TIME_FORMAT


class MovieSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format=DATE_TIME_FORMAT, read_only=True)
    updated = serializers.DateTimeField(format=DATE_TIME_FORMAT, read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', "is_favorite", "updated", "created", "title", "release_date"]

    def get_is_favorite(self, obj):
        user_id = self.context.get('user_id')
        content_type=ContentType.objects.get_for_model(Movie)
        return Favorite.objects.filter(user_id=user_id, object_id=obj.pk, content_type=content_type).exists()


class MovieListSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Movie
        fields = ['id', "is_favorite", "updated", "created", "title", "release_date"]

    def get_is_favorite(self, obj):
        user_id = self.context.get('user_id')
        content_type=ContentType.objects.get_for_model(Movie)
        return Favorite.objects.filter(user_id=user_id, object_id=obj.pk, content_type=content_type).exists()
    
    def get_title(self, obj):
        user_id = self.context.get('user_id')
        content_type=ContentType.objects.get_for_model(Movie)
        favorite_obj = Favorite.objects.filter(user_id=user_id, object_id=obj.pk, content_type=content_type).first()
        # If Custom Title is there, will respond with that, else Title is returned.
        if favorite_obj and favorite_obj.custom_name:
            return favorite_obj.custom_name
        return obj.title
