from rest_framework import serializers
from .models import Author
from .models import Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
	"""
	Serializes all fields of the Book model.
	Includes custom validation to ensure
	publication_year is not in the future.\
	"""
	class Meta:
		model = Book
		fields = ['id', 'title', 'publication_year', 'author']

	#Custom validation
	def validate_publication_year(self, value):
		current_year = datetime.now().year
		if value > current_year:
			raise serializers.ValidationError(
				"Publication year cannot be in the future."
			)
		return value

class AuthorSerializer(serializers.ModelSerializer):
	"""
	Serializes an Author including all related books.
	Uses nested BookSerializer to show book list.
	"""
	books = BookSerializer(many=True, read_only=True) #nested serialization

	class Meta:
		model = Author
		fields = ['id', 'name', 'books']
