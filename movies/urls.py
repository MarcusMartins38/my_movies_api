from django.urls import path

from movies.views import MovieListCreateView, MovieRetrieveUpdateDestroyView

urlpatterns = [
    path('', MovieListCreateView.as_view(), name='movie-list-create'),
    path('<int:pk>/', MovieRetrieveUpdateDestroyView.as_view(), name='movie-detail'),
]