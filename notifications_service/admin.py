from django.contrib import admin

from notifications_service.models import TelegramUser

admin.site.register(TelegramUser)
