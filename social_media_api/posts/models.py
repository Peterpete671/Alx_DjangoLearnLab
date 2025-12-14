from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Post(models.Model):
    """
    Post model representing user posts in the social media platform.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="The user who created this post"
    )
    title = models.CharField(max_length=255, help_text="Post title")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_comments_count(self):
        """Returns the count of comments on this post"""
        return self.comments.count()


class Comment(models.Model):
    """
    Comment model representing user comments on posts.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The user who created this comment"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['post', '-created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='likes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

        def __str__(self):
            return f"{self.user} liked {self.post.id}"
    