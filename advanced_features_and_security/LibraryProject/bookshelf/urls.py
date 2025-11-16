from . import views
from django.urls import path

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('books/delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('example-form/', views.example_form_view, name='example_form'),
]
