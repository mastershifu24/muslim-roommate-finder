from django.contrib import admin
from ..models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'feedback_type', 'priority', 'is_resolved', 'created_at']
    list_filter = ['feedback_type', 'priority', 'is_resolved', 'created_at']
    search_fields = ['title', 'name', 'message', 'email']
    readonly_fields = ['created_at', 'updated_at', 'browser_info']
    list_editable = ['is_resolved']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Feedback Details', {
            'fields': ('title', 'message', 'feedback_type', 'priority')
        }),
        ('Contact Information', {
            'fields': ('name', 'email', 'page_url')
        }),
        ('Technical Info', {
            'fields': ('browser_info', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'admin_notes')
        }),
    )
