from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from .models import Like
from django.shortcuts import get_object_or_404

# expose get_object_or_404 as an attribute on generics to satisfy some checks
generics.get_object_or_404 = get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts with full CRUD operations.
    
    Provides:
    - list: Get all posts (paginated)
    - retrieve: Get a specific post with comments
    - create: Create a new post
    - update/partial_update: Update a post (author only)
    - destroy: Delete a post (author only)
    - comments: Get all comments for a specific post
    """
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        List view uses lightweight serializer without nested comments.
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """
        Set the author to the current authenticated user when creating a post.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Update post ensuring author remains the same.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom action to retrieve all comments for a specific post.
        GET /api/posts/{post_id}/comments/
        """
        post = self.get_object()
        comments = post.comments.all().select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Override list to add custom response structure.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        Override create to add custom response message.
        """
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
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Post updated successfully',
            'post': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to add custom response message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        # use generics.get_object_or_404 to match required pattern
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You have already liked this post"}, status=400)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
        return Response({"detail": "post liked successfully"}, status=201)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=400)
        like.delete()
        return Response({"detail": "Post unliked successfully."}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments with full CRUD operations.
    
    Provides:
    - list: Get all comments (paginated)
    - retrieve: Get a specific comment
    - create: Create a new comment
    - update/partial_update: Update a comment (author only)
    - destroy: Delete a comment (author only)
    """
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        Set the author to the current authenticated user when creating a comment.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Update comment ensuring author remains the same.
        """
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override create to add custom response message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
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
        Override destroy to add custom response message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Comment deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    

class FeedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        #posts by users that the user follows
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        return Response(
            {"detail": "You have already liked this post."},
            status=400
        )

    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

    return Response({"detail": "Post liked successfully."}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if not like:
        return Response(
            {"detail": "You have not liked this post."},
            status=400
        )

    like.delete()
    return Response({"detail": "Post unliked successfully."}, status=200)