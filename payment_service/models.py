from django.db import models
from django.utils.translation import gettext_lazy as _
from borrowing_service.models import Borrowing


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
    session_url = models.URLField(null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    money_to_be_paid = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
