from django.db import transaction
from rest_framework import serializers
from payments.helper import create_stripe_payment
from payments.models import Payment
from payments.serializers import PaymentSerializer
from telegram_helper import send_message
from books.models import Book
from borrow.models import Borrow
from user.serializers import UserSerializer


class BorrowSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user = UserSerializer(read_only=True)
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )

    def validate_book(self, book):
        if self.instance is None and book.inventory <= 0:
            raise serializers.ValidationError("There is no book to borrow")
        return book

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context["request"].user
            book = validated_data["book"]

            book.inventory -= 1
            book.save()
            message = f"""
            The book {book.title} has been borrowed by {user.email}"""
            send_message(message)

            borrow = Borrow.objects.create(user=user, **validated_data)
            payment = create_stripe_payment(borrow)
            return payment.session_url

    def update(self, instance, validated_data):
        if (
            "actual_return_date" in validated_data
            and validated_data["actual_return_date"]
        ):
            instance.book.inventory += 1
            instance.book.save()

        return super().update(instance, validated_data)

    def get_payments(self, obj):
        payments = Payment.objects.filter(borrowing=obj)
        return PaymentSerializer(payments, many=True).data
