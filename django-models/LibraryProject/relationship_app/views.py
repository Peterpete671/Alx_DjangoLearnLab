from django.shortcuts import render
from django.views.generic import ListView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: list all books in a specific library
class LibraryBookListView(ListView):
    model = Book
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'books'

    def get_queryset(self):
        # Get the library id from URL
        library_id = self.kwargs.get('pk')
        return Book.objects.filter(library_id=library_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library'] = Library.objects.get(pk=self.kwargs.get('pk'))
        return context
