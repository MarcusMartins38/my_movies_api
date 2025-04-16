from rest_framework import generics, permissions, filters

from movies.models import Movie
from movies.serializers import MovieSerializer

class MovieListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'rate']
    ordering = ['-created_at']

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user)