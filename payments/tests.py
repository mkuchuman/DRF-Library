from django.test import TestCase
from rest_framework.test import APITestCase
from unittest import mock
from payments.models import Payment
from borrow.models import Borrow
from payments.serializers import PaymentSerializer
from decimal import Decimal
from django.utils import timezone
from books.models import Book
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class PaymentModelTest(TestCase):
    def setUp(self):
        book = Book.objects.create(title="Test Book", daily_fee=10, inventory=5)
        user = get_user_model().objects.create_user(email="user@example.com", password="testpassword")
        self.borrow = Borrow.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=7),
            book=book,
            user=user
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            status=Payment.PaymentStatus.PENDING,
            type=Payment.PaymentType.PAYMENT,
            borrowing=self.borrow,
            session_url="https://example.com/session",
            session_id="sess_123",
            amount=Decimal("29.99"),
        )
        self.assertEqual(payment.status, Payment.PaymentStatus.PENDING)
        self.assertEqual(payment.type, Payment.PaymentType.PAYMENT)
        self.assertEqual(payment.borrowing, self.borrow)
        self.assertEqual(payment.amount, Decimal("29.99"))


class PaymentSerializerTest(TestCase):
    def setUp(self):

        book = Book.objects.create(title="Test Book", daily_fee=10, inventory=5)
        user = get_user_model().objects.create_user(email="user@example.com", password="testpassword")
        self.borrow = Borrow.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=7),
            book=book,
            user=user
        )
        self.payment = Payment.objects.create(
            status=Payment.PaymentStatus.PENDING,
            type=Payment.PaymentType.PAYMENT,
            borrowing=self.borrow,
            session_url="https://example.com/session",
            session_id="sess_123",
            amount=Decimal("29.99"),
        )

    def test_payment_serializer(self):
        serializer = PaymentSerializer(self.payment)
        data = serializer.data
        self.assertEqual(data["status"], Payment.PaymentStatus.PENDING)
        self.assertEqual(data["type"], Payment.PaymentType.PAYMENT)
        self.assertEqual(data["amount"], "29.99")


class PaymentViewSetTest(APITestCase):
    def setUp(self):
        book = Book.objects.create(title="Test Book", daily_fee=10, inventory=5)
        self.user = get_user_model().objects.create_user(email="user@example.com", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.borrow = Borrow.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=7),
            book=book,
            user=self.user
        )
        self.payment = Payment.objects.create(
            status=Payment.PaymentStatus.PENDING,
            type=Payment.PaymentType.PAYMENT,
            borrowing=self.borrow,
            session_url="https://example.com/session",
            session_id="sess_123",
            amount=Decimal("29.99"),
        )

class StripePaymentTest(TestCase):
    @mock.patch("stripe.checkout.Session.create")
    def test_create_stripe_session(self, mock_stripe_session_create):
        mock_stripe_session_create.return_value = mock.Mock(id="sess_test123", url="https://example.com/session")

        from payments.helper import create_stripe_payment
        book = Book.objects.create(title="Test Book", daily_fee=10, inventory=5)
        user = get_user_model().objects.create_user(email="user@example.com", password="testpassword")
        borrow = Borrow.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=7),
            actual_return_date=timezone.now().date() + timezone.timedelta(days=14),
            book=book,
            user=user
        )

        payment = create_stripe_payment(borrow)
        self.assertEqual(payment.session_id, "sess_test123")
        self.assertEqual(payment.session_url, "https://example.com/session")
        self.assertEqual(payment.amount, 140)
