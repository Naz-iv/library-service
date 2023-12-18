from django.test import TestCase
from payment_service.services import get_checkout_session
from borrowing_service.models import Borrowing, Book
from payment_service.models import Payment, PaymentStatus, PaymentTypes
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timedelta


class ServicesTestCase(TestCase):
    def setUp(self):
        book = Book.objects.create(
            title="Test Book",
            daily_fee=Decimal("5.00"),
        )

        self.borrowing = Borrowing.objects.create(
            book=book,
            borrow_date=datetime.now() - timedelta(days=10),
            expected_return_date=datetime.now() + timedelta(days=7),
        )

        self.payment = Payment.objects.create(
            borrowing=self.borrowing,
            payment_type=PaymentTypes.PAYMENT,
            status=PaymentStatus.PENDING,
        )

    def test_get_checkout_session(self):
        session = get_checkout_session(self.borrowing, self.payment.id)
        success_url = reverse(
            "payment_service:payments-payment-successful", args=[self.payment.id]
        )
        cancel_url = reverse(
            "payment_service:payments-payment-canceled", args=[self.payment.id]
        )

        self.assertEqual(session.success_url, "http://testserver" + success_url)
        self.assertEqual(session.cancel_url, "http://testserver" + cancel_url)
