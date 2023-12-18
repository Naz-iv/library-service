from django.test import TestCase
from payment_service.services import calculate_payment_amount, calculate_fine_amount
from borrowing_service.models import Borrowing
from decimal import Decimal
from datetime import datetime, timedelta


class CalculationsTestCase(TestCase):
    def test_calculate_payment_amount(self):
        book_price = Decimal("10.00")
        borrowing_days = 5
        borrowing = Borrowing(
            expected_return_date=datetime.now() + timedelta(days=borrowing_days),
            book__daily_fee=book_price,
        )
        result = calculate_payment_amount(borrowing)
        expected_result = int(book_price * borrowing_days * 100)
        self.assertEqual(result, expected_result)

    def test_calculate_fine_amount(self):
        book_price = Decimal("10.00")
        overdue_days = 3
        borrowing = Borrowing(
            expected_return_date=datetime.now() - timedelta(days=overdue_days),
            actual_return_date=datetime.now(),
            book__daily_fee=book_price,
        )
        result = calculate_fine_amount(borrowing)
        expected_result = int(book_price * 2 * overdue_days * 100)
        self.assertEqual(result, expected_result)
