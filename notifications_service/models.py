from django.db import models

from customer.models import Customer


class TelegramUser(models.Model):
    user_id = models.ForeignKey(Customer,
                                on_delete=models.CASCADE,
                                related_name="customer")
    chat_id = models.IntegerField(unique=True)
