from rest_framework import permissions
from .auth import user_can_access_conversation, user_can_access_message


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
