from django.db import transaction
from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from borrow.models import Borrow
from user.serializers import UserSerializer


class BorrowSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all()
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
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

            borrow = Borrow.objects.create(user=user, **validated_data)
            return borrow

    def update(self, instance, validated_data):
        if (
            "actual_return_date" in validated_data
            and validated_data["actual_return_date"]
        ):
            instance.book.inventory += 1
            instance.book.save()

        return super().update(instance, validated_data)
