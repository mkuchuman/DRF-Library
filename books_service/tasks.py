from django.utils import timezone

from django_q.tasks import schedule

from borrow.models import Borrow
from telegram_helper import send_message


def check_overdue_borrowings():
    overdue_borrowings = Borrow.objects.filter(
        expected_return_date__lte=timezone.now().date(), actual_return_date=None
    )
    if overdue_borrowings:
        for borrow in overdue_borrowings:
            message = (
                f"The borrowing {borrow.book.title} by {borrow.user.email} is overdue"
            )
            send_message(message)
    else:
        send_message("No borrowings overdue found")


schedule(
    "books_service.tasks.check_overdue_borrowings",
    schedule_type="I",  # Interval
    minutes=1,
)
