from rest_framework import viewsets, permissions

from cakes.models import Cake
from review.models import Review

from .serializers import CakeListSerializer, ReviewSerializer


# Create your views here.
class CakeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cake.objects.select_related('category').all()
    serializer_class = CakeListSerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Review.objects.select_related('cake', 'user').all()
        cake = self.request.query_params.get('cake')
        if cake:
            qs = qs.filter(cake_id=cake)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
