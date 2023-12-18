from django.utils import timezone

from borrowing_service.models import Borrowing


def calculate_fine_amount(borrowing: Borrowing) -> int:
    """
    Calculates amount user would have to pay
    for overdue on the current date
    """
    overdue_days = (timezone.now().date
                    - borrowing.expected_return_date).days
    book_price = borrowing.book.daily_fee
    return int(book_price * 2 * overdue_days * 100)
