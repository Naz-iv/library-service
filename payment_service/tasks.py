import stripe
from celery import shared_task

from payment_service.models import Payment


def check_if_session_expired(session_id: str) -> bool:
    """Check is session status is expired"""
    session = stripe.checkout.Session.retrieve(session_id)
    status = session.get("payment_intent", {}).get("status")
    if status == "expired":
        return True
    return False


@shared_task
def verify_session_status() -> None:
    """Verify if pending sessions did not expire"""
    payments = Payment.objects.filter(status=Payment.PaymentStatus.PENDING)

    for payment in payments:
        if check_if_session_expired(payment.session_id):
            payment.status = Payment.PaymentStatus.EXPIRED
            payment.save()
