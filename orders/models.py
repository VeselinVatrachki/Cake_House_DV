from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from cakes.models import Cake


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        DONE = 'done', 'Done'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    note = models.TextField(blank=True)
    event_date = models.DateField(help_text='Preferred pickup or event date.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} by {self.user.get_username()}'

    @property
    def total(self) -> Decimal:
        return sum((line.line_total() for line in self.lines.all()), Decimal('0'))


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='lines',
    )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.PROTECT,
        related_name='order_lines',
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['id']

    def clean(self):
        super().clean()
        if self.quantity is not None and self.quantity < 1:
            raise ValidationError({'quantity': 'Quantity must be at least 1.'})

    def line_total(self) -> Decimal:
        return self.cake.price * self.quantity
