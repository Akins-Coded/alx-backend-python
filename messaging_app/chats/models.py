from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds UUID as primary key, phone number, and user role field.
    """

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
        )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
        USER = 'USER', 'User'

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        names = ', '.join([u.username for u in self.participants.all()])
        return (
            f"Conversation {self.conversation_id} with "
            f"{self.participants.count()} participants: {names}"
        )


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    conversation = models.ForeignKey(
        Conversation, related_name='messages', on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"
