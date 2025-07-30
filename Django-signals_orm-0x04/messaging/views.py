from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Notification, MessageHistory
from .serializers import MessageSerializer, NotificationSerializer, MessageHistorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response

def build_threaded_message(message): # Helper function to build threaded message structure
        return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": [build_threaded_message(reply) for reply in message.replies.all()]
    }

   
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('sender', 'receiver', 'edited_by', 'parent_message')\
                                     .prefetch_related('replies')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'receiver', 'is_read', 'edited']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

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
