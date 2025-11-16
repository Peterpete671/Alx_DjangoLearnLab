import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "J.K. Rowling"  # Replace with actual author name
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)  # Use filter for checks
    print(f"Books by {author.name}:")
    for book in books_by_author:
        print(f"- {book.title}")
except Author.DoesNotExist:
    print(f"No author found with the name '{author_name}'")

#  List all books in a specific library

library_name = "Central Library"  # Replace with actual library name
try:
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"\nBooks in {library.name}:")
    for book in books_in_library:
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"No library found with the name '{library_name}'")

# Retrieve the librarian for a library

try:
    librarian = Librarian.objects.get(library=library)
    print(f"\nLibrarian of {library.name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to {library.name}")
