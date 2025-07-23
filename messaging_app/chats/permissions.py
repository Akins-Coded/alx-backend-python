from rest_framework import permissions
from .auth import user_can_access_conversation, user_can_access_message
from .models import Conversation, Message

class IsOwnerOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow sender or recipient to access the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return user_can_access_conversation(request.user, obj)


class IsOwnerOfMessage(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access its messages.
    """

    def has_object_permission(self, request, view, obj):
        return user_can_access_message(request.user, obj)

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Ensure User is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Handle permission for conversation and message instances
        if instances(obj, Conversation):
            return user_can_access_conversation(request.user, obj)
        
        if isinstance(obj, Message):
            return user_can_access_message(request.user, obj)
        
        return False