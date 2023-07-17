from django_filters import rest_framework as filters
from movies.models import Movie

class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    release_date = filters.DateFilter()
    is_favorite = filters.BooleanFilter(method='filter_by_favorite')

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'is_favorite']

    def filter_by_favorite(self, queryset, name, value):
        user_id = self.request.query_params.get("user_id", None)
        if user_id:
            return queryset.filter(favorites__user_id=user_id)
        else:
            return queryset.none()
