from django.db import IntegrityError
from django.test import TestCase

from book_service.models import Book


class BookModelTest(TestCase):

    def test_book_available_property(self):
        book = Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="soft",
            inventory=3,
            daily_fee=2.00
        )
        self.assertTrue(book.available)

    def test_book_unavailable_property(self):
        book = Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="soft",
            inventory=0,
            daily_fee=2.00
        )
        self.assertFalse(book.available)

    def test_book_unique_togather_fields(self):
        Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="soft",
            inventory=0,
            daily_fee=2.00
        )
        with self.assertRaises(IntegrityError) as error:
            Book.objects.create(
                title="Inferno",
                author="Dan Broun",
                cover="soft",
                inventory=0,
                daily_fee=2.00
            )
            self.assertEqual(
                str(error.exception),
                "UNIQUE constraint failed: book_service_book.title, "
                "book_service_book.author, book_service_book.cover"
            )

    def test_book_ordering(self):
        book1 = Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="soft",
            inventory=2,
            daily_fee=2.00
        )
        book2 = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover="hard",
            inventory=5,
            daily_fee=3.50
        )
        book3 = Book.objects.create(
            title="Inferno",
            author="Other Autor",
            cover="soft",
            inventory=4,
            daily_fee=2.00
        )
        book4 = Book.objects.create(
            title="Inferno",
            author="Dan Broun",
            cover="hard",
            inventory=5,
            daily_fee=2.00
        )

        book_list = [book4, book1, book3, book2]
        books = list(Book.objects.all())

        self.assertEqual(
            book_list, books
        )
