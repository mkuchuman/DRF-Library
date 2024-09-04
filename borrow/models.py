from django.db import models

from books.models import Book
from books_service import settings


class Borrow(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(borrow_date__lte=models.F('expected_return_date')),
                                   name='check_borrow_date_before_return_date')
        ]