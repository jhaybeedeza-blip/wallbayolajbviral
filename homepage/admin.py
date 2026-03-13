from django.contrib import admin
from .models import UnsentMessage

@admin.register(UnsentMessage)
class UnsentMessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'message_preview')
    list_filter = ('created_at',)
    search_fields = ('sender_name', 'receiver_name', 'message_content')
    readonly_fields = ('created_at',)
    
    def message_preview(self, obj):
        """Display a truncated preview of the message"""
        preview = obj.message_content[:75]
        if len(obj.message_content) > 75:
            preview += '...'
        return preview
    message_preview.short_description = 'Message Preview'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('sender_name', 'receiver_name', 'message_content')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

