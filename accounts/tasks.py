import logging

from celery import shared_task
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_notification(user_id: int) -> str:
    """Async welcome step (console log / email hook).

    Receives user_id (int) rather than a User instance because Celery
    serializes task arguments as JSON, which cannot carry ORM objects.
    """
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # User was deleted between task dispatch and execution.
        return 'missing_user'
    logger.info('Welcome task for user %s', user.get_username())
    return 'ok'
