from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_notification(user_id: int) -> str:
    """
    Sends a welcome email to a newly registered user.
    Runs asynchronously using Celery.
    """
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist.")
        return "missing_user"

    try:
        send_mail(
            subject="Welcome to Cake House!",
            message=f"Hi {user.username}, welcome to Cake House! 🎂",
            from_email="noreply@cakehouse.com",
            recipient_list=[user.email],
            fail_silently=True,
        )
        logger.info(f"Welcome email sent to {user.email}")
        return "email_sent"

    except Exception as e:
        logger.error(f"Error sending email to {user.email}: {str(e)}")
        return "email_failed"


@shared_task
def process_order(order_id: int) -> str:
    """
    Simulates background order processing.
    """
    from orders.models import Order  # local import to avoid circular imports

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.error(f"Order with ID {order_id} does not exist.")
        return "missing_order"

    # Simulate processing
    order.status = "processed"
    order.save()

    logger.info(f"Order {order_id} processed successfully.")
    return "order_processed"