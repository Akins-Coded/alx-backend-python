from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def track_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original_message = Message.objects.get(pk=instance.pk)
            if original_message.content != instance.content:
                MessageHistory.objects.create(
                    message=original_message,
                    previous_body=original_message.content,
                    edited_at=now()
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
