import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian



#  Query all books by a specific author
author = Author.objects.first() # Replace with any author instance
books_by_author = author.books.all()
print(f"Books by {author.name}:")
for book in books_by_author:
	print(f"- {book.title}")

#  List all books in a library
library = Library.objects.first() # Replace with any library instance
print(f"\nBooks in {library.name}:")
for book in library.books.all():
	print(f"- {book.title}")

#  Retrieve the librarian for a library
librarian = library.librarian
print(f"\nLibrarian of {library.name}: {librarian.name}")
