from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer,
)
from .permissions import IsAuthorOrReadOnly
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts with full CRUD operation.
    Provides:
    1. list - Get all points, paginated
    2. create - create a new post
    3. retrieve - get a specific post with comments
    4. update or partial_update - update a post
    5. destroy - delete a post
    6. comments - get all comments for a specific post
    update, partial_pudate and destroy can only be performed by the author.
    """
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use different serializers for list and detail views
        """
        if self.action == 'list':
            return PostListSerializer
        return PostListSerializer
    
    def perform_create(self, serializer):
        """
        set the author to the current authenticated user when creating a post.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom action to retrieve all comments for a specific post
        GET api/posts/{post_id}/comments/
        """
        post = self.get_object()
        comments = post.comments.all().select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        """
        Override list to add custom response structure
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(page, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """Override create to add custom response message"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Post created successfully',
            'post': serializer.data
        }, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        """
        Override update to add custom response message.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Post updated successfully',
            'post': serializer.data
        })
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to add custom response message
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing comments with full CRUD operations
    Provides:
    list: get all the comments paginated
    retrieve: get a specific comment
    create: create a new comment
    update/partial_update: update a comment, author only
    destroy: delete a comment, author only
    """
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post','author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        Set the author to the current authenticated user when creating a comment.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
       """
       Update comment ensuring author remains the same
       """
       serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override create to add custom response message
        """
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform.create(serializer)

        return Response({
            'message': 'Comment created successfully',
            'comment': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Override update to add custom response message.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Comment updated successfully',
            'comment': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to add custom response message
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Comment deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)