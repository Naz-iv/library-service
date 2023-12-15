from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from borrowing_service.models import Borrowing

logger = get_task_logger(__name__)


@shared_task(name="check_overdue_task")
def check_overdue_task(self):
    borrowings = Borrowing.objects.filter(
        expected_return_date__lte=timezone.now()+timezone.timedelta(days=1),
        is_active=True
    )
    if len(borrowings):
        for borrowing in borrowings.all():
            """Send a notification"""
            pass
    else:
        """Send a notification"""
        pass
    return "Done sending notifications!"
