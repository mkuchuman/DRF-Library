from django.db import models

from borrow.models import Borrow


# Create your models here.
class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING'
        PAID = 'PAID'

    class PaymentType(models.TextChoices):
        PAYMENT = 'PAYMENT'
        FINE = 'FINE'

    status = models.CharField(
        max_length=7,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    type = models.CharField(
        max_length=7,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT
    )
    borrowing = models.ForeignKey(Borrow, on_delete=models.CASCADE)
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
