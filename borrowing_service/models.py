from django.db import models

from book_service.models import Book
from core import settings


class Borrowing(models.Model):
    BORROW_TERM = 14
    borrow_date = models.DateField(auto_now_add=True)
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.OneToOneField(Book, on_delete=models.CASCADE,
                                primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="borrowings")

    class Meta:
        ordering = ["-borrow_date"]
