# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # Post CRUD URLs
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),

    # Comment URLs
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

    # Posts by tag
    path("tags/<str:tag_name>/", views.PostByTagListView.as_view(), name="posts_by_tag"),
]
