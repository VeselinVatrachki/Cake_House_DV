from django.db import models
from django.conf import settings

from cakes.models import Cake


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.get_username()} - {self.cake.name}'
