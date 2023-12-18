from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

from book_service.models import Book
from core import settings


BORROW_TERM = timezone.timedelta(days=14)


def set_expected_return_date():
    return (timezone.now() + BORROW_TERM).date()


class BorrowingManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related("book", "user")


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(default=set_expected_return_date)
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name="borrowings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="borrowings")
    is_active = models.BooleanField(default=True)

    objects = BorrowingManager()

    class Meta:
        ordering = ["-is_active", "-borrow_date"]

    def __str__(self):
        return f"{self.user} borrowed {self.book.title}"
