from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from book_service.serializers import BookListSerializer, BookSerializer

BOOK_URL = reverse("book_service:book-list")


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list_does_not_require_authentication(self):
        Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="soft",
            inventory=2,
            daily_fee=2.00
        )
        Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover="hard",
            inventory=5,
            daily_fee=3.50
        )
        books = BookListSerializer(Book.objects.all(), many=True)
        response = self.client.get(BOOK_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, books.data)

    def test_book_create_forbidden(self):
        response = self.client.post(BOOK_URL, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            username="user", password="password123"
        )
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="soft",
            inventory=2,
            daily_fee=2.00
        )
        self.book2 = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover="hard",
            inventory=5,
            daily_fee=3.50
        )

    def test_book_list_available(self):
        response = self.client.get(BOOK_URL)
        books = BookListSerializer(Book.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, books.data)

    def test_book_create_forbidden(self):
        response = self.client.post(BOOK_URL, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_filter_by_title(self):
        serializer = BookListSerializer(
            Book.objects.filter(
                title__icontains="Inferno"
            ),
            many=True
        )
        response = self.client.get(BOOK_URL, {"title": "Inferno"})
        self.assertEqual(response.data, serializer.data)

    def test_book_filter_by_author(self):
        serializer = BookListSerializer(
            Book.objects.filter(
                author__icontains="Scott"
            ),
            many=True
        )
        response = self.client.get(BOOK_URL, {"author": "Scott"})
        self.assertEqual(response.data, serializer.data)


class AdminApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            username="user", password="password123", is_staff=True
        )
        self.client.force_login(self.user)
        self.book = Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="soft",
            inventory=2,
            daily_fee=2.00
        )

    def test_book_create_as_admin(self):
        payload = {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "cover": "hard",
            "inventory": 5,
            "daily_fee": "3.50"
        }

        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_update_as_admin(self):
        payload = {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "cover": "hard",
            "inventory": 5,
            "daily_fee": "3.50"
        }

        response = self.client.patch(
            reverse(
                "book_service:book-detail",
                args=[self.book.id]),
            payload)

        book = BookSerializer(Book.objects.get(id=self.book.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            book.data,
            payload
        )

    def test_book_delete_as_admin(self):
        response = self.client.delete(reverse(
            "book_service:book-detail",
            args=[self.book.id]
        ))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Book.objects.get(id=self.book.id)
