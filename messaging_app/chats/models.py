from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # Extend the User model if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.username

    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', ('Admin')
        STAFF = 'STAFF', ('Staff')
        USER = 'USER', ('User')

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )
    def __str__(self):
        return f"{self.username} ({self.role})"

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_names = ', '.join([user.username for user in self.participants.all()])
        return f"Conversation {self.id} with {self.participants.count()} participants{participant_names}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
    

