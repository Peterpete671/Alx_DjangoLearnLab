from django.urls import path
from . import views

urlpatterns = [
    # Function-based view URL
    path('books/', views.list_books, name='list_books'),

    # Class-based view URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
