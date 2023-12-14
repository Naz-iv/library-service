from datetime import timedelta

from django.db import models

from book_service.models import Book
from core import settings


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    actual_return_date = models.DateTimeField()
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="borrowings")

    class Meta:
        ordering = ["-borrow_date"]

    @property
    def expected_return_date(self):
        return self.borrow_date.date + timedelta(days=14)
