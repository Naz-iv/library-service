from __future__ import absolute_import, unicode_literals

from celery import task
from celery.utils.log import get_task_logger

from borrowing_service.utils import check_overdue

logger = get_task_logger(__name__)


@task(name="check_overdue_task")
def check_overdue_task(borrowing):
    logger.info("Check borrowing overdue")
    return check_overdue(borrowing)
