from .models import Notification,Order
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=Order)
def create_order_notification(sender,instance,created, **kwargs):

    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Your order #{instance.id} has been created"
        )