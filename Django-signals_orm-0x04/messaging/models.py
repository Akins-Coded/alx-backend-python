import uuid
from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager
User = get_user_model()

# Create your models here

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messaging_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)
    parent_message = models.ForeignKey(  # New field for threaded replies
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages  
    class Meta:
        ordering = ['-timestamp']  # Order messages by timestamp, newest first
        verbose_name_plural = 'Messages'
        verbose_name = 'Message'

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} regarding message {self.message.id}"

class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, related_name='edit_history', on_delete=models.CASCADE)
    previous_body = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id} edited at {self.edited_at}"


