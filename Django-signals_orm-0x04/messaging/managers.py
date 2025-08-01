# managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.get_queryset().filter(receiver=user, is_read=False) \
                   .select_related('sender') \
                   .only('id', 'content', 'timestamp', 'sender__username')
