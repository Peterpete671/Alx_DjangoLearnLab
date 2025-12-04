from django.db import models

# Create your models here.
class Author(models.Model):
	"""
	Stores information about a book author.
	- name: The author's full name.
	- Relationship: One author can have many books
	"""
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Book(models.Model):
	"""
	Represents a book.
	-title: The name of the book.
	-publication_year: Year the book was released
	-author: ForeignKey establishing one-to-many with Author
	"""
	title = models.CharField(max_length=255)
	publication_year = models.IntegerField()
	author = models.ForeignKey(
		Author,
		on_delete=models.CASCADE,
		related_name="books"
	)

	def __str__(self):
		return self.title
