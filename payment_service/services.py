import stripe
from decimal import Decimal

from stripe.checkout import Session

from borrowing_service.models import Borrowing
from core import settings
from payment_service.models import Payment


def calculate_payment_amount(borrowing: Borrowing) -> int:
    """Calculates amount user has to pay for borrowing"""
    borrowing_days = (borrowing.expected_return_date.date()
                      - borrowing.borrow_date).days
    book_price = borrowing.book.daily_fee
    return int(book_price * borrowing_days * 100)


def calculate_fine_amount(borrowing: Borrowing) -> int:
    """Calculates amount user has to pay for overdue expected return date"""
    overdue_days = (borrowing.actual_return_date.date()
                    - borrowing.expected_return_date).days
    book_price = borrowing.book.daily_fee
    return int(book_price * 2 * overdue_days * 100)


def get_checkout_session(borrowing: Borrowing) -> Session:
    if (
        borrowing.actual_return_date
        and borrowing.actual_return_date > borrowing.expected_return_date
    ):
        payment_amount = calculate_fine_amount(borrowing)
    else:
        payment_amount = calculate_payment_amount(borrowing)

    return Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": stripe.Price.create(
                    currency="usd",
                    unit_amount=payment_amount,
                    product_data={
                        "name": borrowing.book.title
                    },
                ),
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=settings.DOMAIN + "/success/",
        cancel_url=settings.DOMAIN + "/cancel/",
    )


def get_payment(borrowing: Borrowing) -> Payment:
    """Create payment instance for borrowing"""
    checkout_session = get_checkout_session(borrowing)
    if (
        borrowing.actual_return_date
        and borrowing.actual_return_date > borrowing.expected_return_date
    ):
        payment_type = Payment.PaymentTypes.FINE
    else:
        payment_type = Payment.PaymentTypes.PAYMENT

    return Payment.objects.create(
        borrowing=borrowing,
        payment_type=payment_type,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_be_paid=checkout_session.amount_total,
    )
