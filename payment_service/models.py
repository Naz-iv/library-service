from django.db import models
from django.utils.translation import gettext_lazy as _
from borrowing_service.models import Borrowing
from core import settings


class Session(models.Model):
    class Currencies(models.TextChoices):
        DOLLAR = "DOLLAR", _("usd")
        HRYVNIA = "HRYVNIA", _("uah")
        EURO = "EURO", _("eur")
        POUND_STERLING = "POUND_STERLING", _("gbp")

    class PaymentModes(models.TextChoices):
        PAYMENT = "PAYMENT", _("payment")
        SETUP = "SETUP", _("setup")
        SUBSCRIPTION = "SUBSCRIPTION", _("subscription")

    class PaymentStatus(models.TextChoices):
        NO_PAYMENT_REQUIRED = "NO_PAYMENT_REQUIRED", _("no_payment_required")
        PAID = "PAID", _("paid")
        UNPAID = "UNPAID", _("unpaid")

    class SessionStatus(models.TextChoices):
        COMPLETED = "COMPLETED", _("completed")
        EXPIRED = "EXPIRED", _("expired")
        OPEN = "OPEN", _("open")

    stripe_session_id = models.CharField(max_length=255)
    currency = models.CharField(
        choices=Currencies.choices, default=Currencies.DOLLAR, max_length=25
    )
    customer_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    borrowing_overdue = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    mode = models.CharField(
        choices=PaymentModes.choices,
        default=PaymentModes.PAYMENT,
        max_length=30
    )
    payment_status = models.CharField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
        max_length=40
    )
    status = models.CharField(
        choices=SessionStatus.choices,
        default=SessionStatus.OPEN,
        max_length=40
    )


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("pending")
        PAID = "PAID", _("paid")

    class PaymentTypes(models.TextChoices):
        PAYMENT = "PAYMENT", _("payment")
        FINE = "FINE", _("fine")

    status = models.CharField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        max_length=40
    )
    payment_type = models.CharField(
        choices=PaymentTypes.choices,
        default=PaymentTypes.PAYMENT,
        max_length=40
    )
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField()
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="payments"
    )
    money_to_be_paid = models.DecimalField(max_digits=10000, decimal_places=2)
