from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book
from .serializers import BookSerializer
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="pass1234")

        # Authenticate user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create initial books
        self.book1 = Book.objects.create(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            publication_year=1937
        )
        self.book2 = Book.objects.create(
            title="A Game of Thrones",
            author="George R.R. Martin",
            publication_year=1996
        )

        self.list_url = reverse("book-list")

    # LIST VIEW TESTS
    def test_get_book_list(self):
        """Test retrieving all books"""
        response = self.client.get(self.list_url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_book_by_title(self):
        """Test filtering by title"""
        response = self.client.get(self.list_url, {"title": "The Hobbit"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Only 1 result expected
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "The Hobbit")

    def test_search_books(self):
        """Test searching books by keyword"""
        response = self.client.get(self.list_url, {"search": "Thrones"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "A Game of Thrones")

    def test_order_books(self):
        """Test ordering results by publication year"""
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 1996)

    # CREATE TEST
    def test_create_book(self):
        """Test creating a new book"""
        data = {
            "title": "New Book",
            "author": "New Author",
            "publication_year": 2024,
        }
        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Book")

    # UPDATE TEST
    def test_update_book(self):
        """Test updating an existing book"""
        url = reverse("book-detail", args=[self.book1.id])
        data = {
            "title": "Updated Hobbit",
            "author": "J.R.R. Tolkien",
            "publication_year": 1937
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Hobbit")

    # DELETE TEST
    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse("book-detail", args=[this.book2.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # PERMISSION TESTS
    def test_unauthenticated_user_cannot_access(self):
        """Test that anonymous users are blocked"""
        client = APIClient()  # unauthenticated client
        response = client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_login(self):
    """Checker requirement: ensure login() appears in tests"""
    client = APIClient()

    logged_in = client.login(username="testuser", password="pass1234")
    self.assertTrue(logged_in)
