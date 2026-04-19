from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Cake(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cakes/')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cake = models.ForeignKey('Cake', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'cake')