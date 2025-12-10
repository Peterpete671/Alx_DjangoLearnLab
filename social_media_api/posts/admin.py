from django.contrib import admin
from .models import Post
from .models import Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin config for post model
    """
    list_display = ['title', 'author', 'created_at', 'updated_at', 'get_comments_count']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
    ('Post Information', {
        'fields': ('author', 'title', 'content')
    }),
    ('Timestamps', {
        'fields': ('created_at', 'updated_at'),
        'classes': ('collapse',)
    }),
    )

    def get_comments_count(self, obj):
        """
        display comment count in admin list 
        """
        return obj.get_comments_count()
    get_comments_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin config for current model
    """
    list_display = ['author', 'post', 'content_preview', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        """Display truncated content in admin list"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'