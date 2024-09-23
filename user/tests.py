from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):

    def test_create_user(self):
        email = 'user@example.com'
        password = 'testpass123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = 'superuser@example.com'
        password = 'superpass123'
        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='testpass123')

    def test_create_superuser_with_is_staff_false(self):
        email = 'superuser@example.com'
        password = 'superpass123'
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=email, password=password, is_staff=False)

    def test_create_superuser_with_is_superuser_false(self):
        email = 'superuser@example.com'
        password = 'superpass123'
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=email, password=password, is_superuser=False)
