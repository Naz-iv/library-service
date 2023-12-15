from datetime import datetime, timedelta
from decimal import Decimal

from borrowing_service.models import Borrowing


def calculate_payment_amount(borrowing: Borrowing) -> Decimal:
    """Calculates amount user has to pay for borrowing"""
    borrowing_days = (
        borrowing.expected_return_date - borrowing.borrow_date
    ).days
    book_price = borrowing.book.daily_fee
    return round(book_price * borrowing_days * 100, 2)


def calculate_fine_amount(borrowing: Borrowing) -> Decimal:
    """Calculates amount user has to pay for overdue expected return date"""
    overdue_days = (
        borrowing.actual_return_date - borrowing.expected_return_date
    ).days
    book_price = borrowing.book.daily_fee
    return round(book_price * 2 * overdue_days * 100, 2)
