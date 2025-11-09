from django.shortcuts import render
from .models import Book, Library

# Create your views here.
#Function-based view to list all books
def list_books(request):
	books = Book.objects.all()
	return render(request, 'list_books.html', {'books': books})

from django.vies.generic import DetailView
from .models import Library

#Class-based view to show library details
class LibraryDetailView(DetailView):
	model = Library
	template_name = 'library_detail.html'
	context_object_name = 'library'
