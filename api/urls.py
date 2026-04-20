from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

# DefaultRouter also exposes a browsable API root at /api/.
router = DefaultRouter()
router.register(r'cakes', views.CakeViewSet, basename='cakes')
router.register(r'reviews', views.ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
