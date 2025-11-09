import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Example: Get a Library by name
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"Library found: {library.name}")
except Library.DoesNotExist:
    print(f"No library found with the name '{library_name}'")

# 1. Query all books by a specific author
author_name = "J.K. Rowling"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = author.books.all()
    print(f"\nBooks by {author.name}:")
    for book in books_by_author:
        print(f"- {book.title}")
except Author.DoesNotExist:
    print(f"No author found with the name '{author_name}'")

# 2. List all books in a library
print(f"\nBooks in {library.name}:")
for book in library.books.all():
    print(f"- {book.title}")

# 3. Retrieve the librarian for a library
try:
    librarian = library.librarian
    print(f"\nLibrarian of {library.name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to {library.name}")

