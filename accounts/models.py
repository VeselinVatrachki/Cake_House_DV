from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    # is_baker = models.BooleanField(default=False)

    display_name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Display name.',
    )

    def get_public_name(self):
        return self.display_name.strip() or self.get_username()

    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'pk': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.TextField(blank=True),
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    favorite_tags = models.ManyToManyField(
        'cakes.Tag',
        blank=True,
        related_name='favorited_by_profiles',
    )

    def __str__(self):
        return f'Profile of {self.user.get_username()}'