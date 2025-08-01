import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender_id = django_filters.NumberFilter(field_name='sender__id', lookup_expr='exact')
    conversation_id = django_filters.NumberFilter(field_name='conversation__id', lookup_expr='exact')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation_id', 'created_after', 'created_before']
