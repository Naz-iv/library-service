import stripe
from celery import shared_task

from payment_service.models import Payment


def check_if_session_expired(session_id: str) -> bool:
    """Check is session status is expired"""
    session = stripe.checkout.Session.retrieve(session_id)

    if session:
        status = session.status

        if status == "expired":
            return True
    return False


def check_if_session_paid(payment) -> bool:
    """Check is session status is expired"""
    session = stripe.checkout.Session.retrieve(payment.session_id)

    if session:
        status = session.status

        if status == "complete":
            return True

    return False


@shared_task
def verify_session_status() -> None:
    """Verify if pending sessions did not expire"""
    payments = Payment.objects.filter(status=Payment.PaymentStatus.PENDING)

    for payment in payments:
        if check_if_session_expired(payment.session_id):
            payment.status = Payment.PaymentStatus.EXPIRED

        if (payment.status == Payment.PaymentStatus.PENDING
                and check_if_session_paid(payment)):
            payment.status = Payment.PaymentStatus.PAID

        payment.save()
