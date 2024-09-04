from rest_framework import serializers

from books.serializers import BookSerializer
from borrow.models import Borrow


class BorrowReadSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

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
