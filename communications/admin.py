from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'timestamp', 'read')
    list_filter = ('read', 'timestamp')
    search_fields = ('subject', 'body', 'sender__username', 'recipient__username')
