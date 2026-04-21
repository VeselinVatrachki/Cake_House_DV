from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from cakes.models import Cake


class Review(models.Model):
    """
    Represents a user review for a specific cake.

    Each user can only review a cake once.
    """
    
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
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # Prevent duplicate reviews (same user + same cake)
        constraints = [
            models.UniqueConstraint(fields=['cake', 'user'], name='unique_review_per_user_cake'),
        ]

    def __str__(self):
        return f'{self.user.get_username()} — {self.cake.name}'

    def clean(self):
        super().clean()
        if self.rating is not None and (self.rating < 1 or self.rating > 5):
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})
