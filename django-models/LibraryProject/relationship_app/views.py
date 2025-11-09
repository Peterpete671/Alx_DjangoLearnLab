from django.http import HttpResponse
from .models import Book
from django.views.generic import DetailView
from .models import Library

# Function-based view: simple text list of books
def list_books(request):
    books = Book.objects.all()
    output = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(output, content_type="text/plain")


# Class-based view: library detail using DetailView
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'  # template can remain for HTML output
    context_object_name = 'library'
