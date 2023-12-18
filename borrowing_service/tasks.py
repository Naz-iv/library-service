from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.contrib.auth import get_user_model

from borrowing_service.models import Borrowing
from borrowing_service.services import calculate_fine_amount
from notifications_service.management.commands.run_telegram_bot import (
    send_notification
)
from notifications_service.models import TelegramUser

logger = get_task_logger(__name__)


@shared_task(bind=True)
def check_overdue_task(self):
    print("Doing stuff")
    borrowings = Borrowing.objects.filter(
        expected_return_date__lte=timezone.now() + timezone.timedelta(days=1),
        is_active=True
    )
    users = [borrowing.user for borrowing in borrowings.all()]
    for borrowing in borrowings:
        borrowing_info = (
            "You have overdue borrowing:\n\n"
            f"-Book: {borrowing.book}\n"
            f"--Borrow date: {borrowing.borrow_date}\n"
            f"--Expected return date: {borrowing.expected_return_date}\n"
            f"--Amount to pay: {calculate_fine_amount(borrowing)}"
        )
        send_notification(
            TelegramUser.objects.get(user_id=borrowing.user.pk).chat_id,
            borrowing_info
        )
    for user in get_user_model().objects.all():
        if user not in users:
            send_notification(
                TelegramUser.objects.get(user_id=borrowing.user.pk).chat_id,
                "No borrowings overdue today!"
            )
    return "Done sending notifications!"
