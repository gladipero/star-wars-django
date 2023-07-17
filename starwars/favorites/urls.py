from django.urls import path
from favorites.views import AddRemoveFavoriteAPIView

urlpatterns = [
    # Other URL patterns
    path('update/<str:object_type>/', AddRemoveFavoriteAPIView.as_view(), name='add_remove_favorite'),
]