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
    Allows only authenticated participants of a conversation to:
    - View (GET)
    - Create (POST)
    - Update (PUT/PATCH)
    - Delete (DELETE)
    """

    def has_permission(self, request, view):
        # Always require authentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return user_can_access_conversation(request.user, obj)

        if isinstance(obj, Message):
            return user_can_access_message(request.user, obj)

        return False


class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['ADMIN', 'STAFF']
        )