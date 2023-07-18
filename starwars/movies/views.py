from rest_framework.generics import ListAPIView
from base.utilities import BasePaginationClass
from movies.models import Movie
from rest_framework.filters import SearchFilter, OrderingFilter
from favorites.models import Favorite
from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, OuterRef
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from movies.serializers import MovieListSerializer


class MovieListAPIView(ListAPIView):
    """
    Movie List API View with filters for title and is_favorite"""
    pagination_class = BasePaginationClass
    queryset = Movie.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'release_date', 'created', 'updated']

    def get(self, request):
        user_id = request.query_params.get("user_id", None)
        is_favorite = self.request.query_params.get("is_favorite", None)
        sort = self.request.query_params.get("sort", "title")
        name = self.request.query_params.get("search")
        # Can also be implemented with Custom Filter Backend  
        favorites_qs = Favorite.objects.filter(
                content_type=ContentType.objects.get_for_model(Movie),
                user_identifier=user_id,
                object_id=OuterRef('id')
            )
        queryset = self.queryset.annotate(is_favorite=Exists(favorites_qs))

        # Used Generic Relation here to search both title and custom name
        if name:
            queryset = queryset.filter(Q(title__icontains=name) | Q(favorite__custom_name__icontains=name))
        
        if is_favorite is not None:
            if is_favorite not in ["true", "false"]:
                return Response({"details": "Valid values for is_favorite filter are true and false only."}, status=status.HTTP_400_BAD_REQUEST)
            is_favorite = is_favorite.lower() == 'true'
            queryset = queryset.filter(is_favorite=is_favorite)
        ## Sort has a default so that pagination gives consistent results always.
        queryset = queryset.order_by(sort)
        queryset = self.filter_queryset(queryset)
    
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        movie_serializer = MovieListSerializer(result_page, many=True, context={'user_id': user_id})
        return paginator.get_paginated_response(movie_serializer.data)
