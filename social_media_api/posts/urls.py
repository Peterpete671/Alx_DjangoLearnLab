from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from .views import FeedView, like_post, unlike_post

app_name = 'posts'

#router and registered viewsets with it
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'posts', PostViewSet)

#API urls are automatically determined by the router
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', like_post, name='post-like'),
    path('posts/<int:pk>/unlike/', unlike_post, name='post-unlike'),
]