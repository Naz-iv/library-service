from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class Customer(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.email
