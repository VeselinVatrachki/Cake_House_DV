from rest_framework import serializers

from cakes.models import Cake
from review.models import Review


class CakeListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Cake
        fields = ('id', 'name', 'slug', 'image', 'price', 'category_name', 'created_at')


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'cake', 'user', 'rating', 'comment', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')