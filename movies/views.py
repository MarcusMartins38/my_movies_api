from rest_framework import generics, permissions, filters
from django.db.models.functions import Lower
from movies.models import Movie
from movies.serializers import MovieSerializer

class MovieListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'rate', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Movie.objects.filter(user=self.request.user)
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        ordering = self.request.query_params.get('ordering')
        if ordering == 'title':
            return queryset.order_by(Lower('title'))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user)