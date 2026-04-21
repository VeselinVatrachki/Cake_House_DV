from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds an optional display_name field used for public-facing pages.
    """

    display_name = models.CharField(
        max_length=150,
        blank=True,
        help_text='Shown on public pages instead of username when set.',
    )

    def get_public_name(self) -> str:
        # Falls back to username so callers never receive an empty string.
        return self.display_name.strip() or self.get_username()

    def get_absolute_url(self):
        return reverse('accounts:public_profile', kwargs={'pk': self.pk})


class Profile(models.Model):
    """
    Profile model linked one-to-one with the User.

    Stores additional user information that doesn't belong
    in the core authentication model.
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=32, blank=True)
    favorite_tags = models.ManyToManyField(
        'cakes.Tag',
        blank=True,
        related_name='favorited_by_profiles',
    )

    def __str__(self):
        return f'Profile of {self.user.get_username()}'
