import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from borrowing_service.models import Borrowing
from payment_service.services import (
    calculate_fine_amount,
    calculate_payment_amount
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        borrowing_id = self.kwargs["borrowing_id"]
        borrowing = get_object_or_404(Borrowing, pk=borrowing_id)

        if (
            borrowing.actual_return_date
            and borrowing.actual_return_date > borrowing.expected_return_date
        ):
            payment_amount = calculate_fine_amount(borrowing)
            product_data = {
                "name": borrowing.book.title,
                "borrowed_date": borrowing.borrow_date,
                "expected_return_date": borrowing.expected_return_date,
                "actual_return_date": borrowing.actual_return_date,
                "days_book_overdue": (
                    borrowing.actual_return_date
                    - borrowing.expected_return_date
                ).days,
            }
        else:
            payment_amount = calculate_payment_amount(borrowing)
            product_data = {
                "name": borrowing.book.title,
                "borrowed_date": borrowing.borrow_date,
                "expected_return_date": borrowing.expected_return_date,
            }

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": {
                        "currency": "usd",
                        "unit_amount": payment_amount,
                        "product_data": product_data,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=settings.DOMAIN + "/success/",
            cancel_url=settings.DOMAIN + "/success/",
        )

        return JsonResponse(checkout_session)
