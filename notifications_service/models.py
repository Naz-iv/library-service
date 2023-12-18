from django.db import models

from core.settings import AUTH_USER_MODEL
from customer.models import Customer


class TelegramUser(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="customer")
    chat_id = models.IntegerField(unique=True)
