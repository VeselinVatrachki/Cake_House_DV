from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile
from .tasks import send_welcome_notification


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=User)
def queue_welcome_task(sender, instance, created, **kwargs):
    if created:
        send_welcome_notification.delay(instance.pk)