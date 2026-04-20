from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User
from .tasks import send_welcome_notification


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Only on first save; subsequent saves are handled by save_profile below.
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # hasattr guard covers the window between user.save() and create_profile()
    # completing during the first request, as well as legacy users with no profile.
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=User)
def queue_welcome_task(sender, instance, created, **kwargs):
    if created:
        send_welcome_notification.delay(instance.pk)
