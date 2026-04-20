from rest_framework import viewsets, permissions

from cakes.models import Cake
from review.models import Review

from .serializers import CakeListSerializer, ReviewSerializer


class CakeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only; cake creation/editing is handled through the web UI, not the API."""

    queryset = Cake.objects.select_related('category').all()
    serializer_class = CakeListSerializer
    # Lookup by slug instead of pk so URLs are human-readable (e.g. /api/cakes/velvet-dream/).
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # Anonymous users can read reviews; writing requires authentication.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Review.objects.select_related('cake', 'user').all()
        # Optional ?cake=<id> query param to filter reviews for a single cake.
        cake = self.request.query_params.get('cake')
        if cake:
            qs = qs.filter(cake_id=cake)
        return qs

    def perform_create(self, serializer):
        # Inject the authenticated user so the client cannot spoof authorship.
        serializer.save(user=self.request.user)
