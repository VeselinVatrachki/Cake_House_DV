from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def validate_image_size(value):
    max_mb = 5
    mb = value.size / (1024 * 1024)
    if mb > max_mb:
        raise ValidationError(f'The image must be less than {max_mb} MB.')
    return value


class Cake(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='cakes/')
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=25.00,
        validators=[MinValueValidator(0.01)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='cakes',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='cakes')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cakes_owned',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):                                  # to generate a link to a specific Cake
        return reverse('cakes:detail', kwargs={'slug': self.slug})
