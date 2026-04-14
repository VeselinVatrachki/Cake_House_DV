from django.db import models

class Cake(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cakes/')
    description = models.TextField()

    def __str__(self):
        return self.name
