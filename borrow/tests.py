from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock
from books.models import Book
from borrow.models import Borrow
from payments.models import Payment
from user.models import User
from decimal import Decimal
from datetime import timedelta


class BorrowViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password")
        self.book = Book.objects.create(
            title="Test Book",
            daily_fee=Decimal("10.00"),
            inventory=5
        )
        self.client.force_authenticate(user=self.user)

    def test_create_borrow(self):
        url = "/api/borrowings/"  # Прямой путь вместо reverse
        borrow_data = {
            "borrow_date": timezone.now().date(),
            "expected_return_date": (timezone.now() + timedelta(days=5)).date(),
            "book": self.book.id
        }
        response = self.client.post(url, borrow_data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)
        self.assertTrue(Borrow.objects.filter(user=self.user, book=self.book).exists())

    def test_return_borrow(self):
        borrow = Borrow.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=(timezone.now() + timedelta(days=1)).date(),
            book=self.book,
            user=self.user
        )
        url = f"/api/borrowings/{borrow.id}/return/"  # Прямой путь вместо reverse
        return_data = {
            "actual_return_date": timezone.now().date(),
        }

        response = self.client.post(url, return_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 6)  # Проверяем, что количество книг восстановилось
