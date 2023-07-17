from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from movies.models import Movie
from planets.models import Planet
from favorites.models import Favorite
from django.contrib.contenttypes.models import ContentType

class AddRemoveFavoriteAPIView(APIView):
    """
    View class to serve API for Adding and removing Favorites for Movie and Planets.
    """
    def post(self, request, object_type):
        object_id = request.data.get("object_id")
        user_id = request.GET.get("user_id")
        if not user_id or not object_id:
            return Response({"details": "User ID and Object ID are a required field"}, status=status.HTTP_400_BAD_REQUEST)
        if object_type == 'movie':
            model = Movie
        elif object_type == 'planet':
            model = Planet
        else:
            return Response({'detail': 'Not supported object type'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = model.objects.get(id=object_id)
        except model.DoesNotExist:
            # Log error e
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the favorite already exists
        content_type=ContentType.objects.get_for_model(model)
        favorite_exists = Favorite.objects.filter(user_id=user_id, content_type=content_type, object_id=object_id).exists()

        if request.data.get('action') == 'add':
            if favorite_exists:
                return Response({'detail': 'Favorite already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new favorite for the current user and the object
            Favorite.objects.create(user_id=user_id, content_object=obj)
            return Response({'detail': 'Action Successfully Executed.'}, status=status.HTTP_201_CREATED)

        elif request.data.get('action') == 'remove':
            if not favorite_exists:
                return Response({'detail': 'Favorite does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the existing favorite
            Favorite.objects.filter(user_id=user_id, content_type=content_type, object_id=object_id).delete()
            return Response({'detail': 'Action Successfully Executed.'}, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
