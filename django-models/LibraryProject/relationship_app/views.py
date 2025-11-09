from django.shortcuts import render, get_object_or_404
from .models import Book, Library
from django.views.generic import DetailView

# --- Function-based view ---
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# --- Class-based view ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
