from .models import Conversation, Message
from django.db.models import Q


def get_user_conversations(user):
    """
    Return conversations where the user is sender or recipient.
    """
    return Conversation.objects.filter(
        Q(participants=user) 
    )

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