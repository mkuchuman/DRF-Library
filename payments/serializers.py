from rest_framework import serializers
from borrow.serializers import BorrowSerializer
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = BorrowSerializer()

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "amount",
        )
