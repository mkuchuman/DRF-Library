from django.utils import timezone

import stripe

from books_service import settings
from payments.models import Payment


def calculate_price(borrow):
    if borrow.actual_return_date:
        date = borrow.actual_return_date
    else:
        date = timezone.now().date()
    days = (date - borrow.borrow_date).days
    total_price = days * borrow.book.daily_fee

    if borrow.expected_return_date < date:
        overdue_days = (date - borrow.expected_return_date).days
        total_price += overdue_days * borrow.book.daily_fee * 2
    return total_price


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment(borrow):
    price = calculate_price(borrow)
    session = stripe.checkout.Session.create(
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": borrow.book.title,
                    },
                    "unit_amount": int(price * 100),
                },
                "quantity": 1,
            }
        ],
    )
    payment = Payment.objects.create(
        status=Payment.PaymentStatus.PENDING,
        type=Payment.PaymentType.PAYMENT,
        borrowing=borrow,
        session_url=session.url,
        session_id=session.id,
        amount=price,
    )

    return payment
