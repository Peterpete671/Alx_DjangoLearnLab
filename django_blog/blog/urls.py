from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post URLs...
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comment URLs...
    path('post/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),

    # Tagging & search URLs
    path('tags/<slug:tag_slug>/', views.TaggedPostListView.as_view(), name='tagged_posts'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
