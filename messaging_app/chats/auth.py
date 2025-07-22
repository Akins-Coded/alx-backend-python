from .models import Conversation, Message
from django.db.models import Q


def get_user_conversations(user):
    """
    Return conversations where the user is sender or recipient.
    """
    return Conversation.objects.filter(
        Q(sender=user) | Q(recipient=user)
    )


def get_user_messages(user, status=None):
    """
    Return messages where the user is either the sender or recipient in the conversation.
    Optionally filter by read/unread status.
    """
    queryset = Message.objects.filter(
        Q(conversation__sender=user) | Q(conversation__recipient=user)
    )

    if status:
        status = status.lower()
        if status == 'read':
            queryset = queryset.filter(is_read=True)
        elif status == 'unread':
            queryset = queryset.filter(is_read=False)

    return queryset



def user_can_access_conversation(user, conversation: Conversation) -> bool:
    """
    Check if the user is the sender or recipient of the conversation.
    """
    return conversation.sender == user or conversation.recipient == user


def user_can_access_message(user, message: Message) -> bool:
    """
    Check if the user is the sender or recipient of the message's conversation.
    """
    conversation = message.conversation
    return conversation.sender == user or conversation.recipient == user