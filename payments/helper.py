from django.http import HttpRequest
from django.urls import reverse
from django.utils import timezone
import stripe
from books_service import settings
from payments.models import Payment


def calculate_price(borrow):
    if borrow.actual_return_date:
        date = borrow.actual_return_date
    else:
        date = borrow.expected_return_date
    days = (date - borrow.borrow_date).days
    total_price = days * borrow.book.daily_fee

    if borrow.expected_return_date < date:
        overdue_days = (date - borrow.expected_return_date).days
        total_price = overdue_days * borrow.book.daily_fee * 2
    return total_price


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment(borrow):
    price = calculate_price(borrow)
    session = stripe.checkout.Session.create(
        mode="payment",
        success_url="http://127.0.0.1:8000/api/payments/payment-succes/{CHECKOUT_SESSION_ID}/",
        cancel_url="http://127.0.0.1:8000/api/payments/payment-cancelled/",
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
    if borrow.actual_return_date and borrow.expected_return_date < borrow.actual_return_date:
            payment.type = Payment.PaymentType.FINE
            payment.save()

    return payment
