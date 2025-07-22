from rest_framework import permissions


class IsOwnerOfConversation(permissions.BasePermission):
    """
    Allows access only to users who are part of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient


class IsOwnerOfMessage(permissions.BasePermission):
    """
    Allows access only to users who are part of the message's conversation.
    Assumes `obj.conversation.sender` and `obj.conversation.recipient` exist.
    """

    def has_object_permission(self, request, view, obj):
        conversation = obj.conversation
        return (
            request.user == conversation.sender or
            request.user == conversation.recipient
        )
