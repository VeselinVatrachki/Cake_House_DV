import logging

from celery import shared_task
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_notification(user_id: int) -> str:
    """Async welcome step (console log / email hook)."""
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return 'missing_user'
    logger.info('Welcome task for user %s', user.get_username())
    return 'ok'
