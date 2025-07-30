from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Notification, MessageHistory, UnreadMessagesManager
from .serializers import MessageSerializer, NotificationSerializer, MessageHistorySerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

def build_threaded_message(message): # Helper function to build threaded message structure
        return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": [build_threaded_message(reply) for reply in message.replies.all()]
    }

class ConversationMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60))  # ⏱ cache for 60 seconds
    def get(self, request, conversation_id):
        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
   
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'receiver', 'is_read', 'edited']

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) \
            .select_related('sender', 'receiver', 'edited_by', 'parent_message') \
            .prefetch_related('replies')

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user) # sender=request.user

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.edited = True
        instance.edited_by = self.request.user
        instance.save()

    @action(detail=True, methods=['get'])
    def thread(self, request, pk=None):
        message = self.get_object()
        threaded = build_threaded_message(message)
        return Response(threaded)

class UnreadMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        unread_messages = Message.unread.unread_for_user(user) # Explicitly using .only() 
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'is_read']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageHistory.objects.all().order_by('-edited_at')
    serializer_class = MessageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['message']

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete_user(self, request):
        user = request.user
        username = user.username
        user.delete()
        return Response({"detail": f"User '{username}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
