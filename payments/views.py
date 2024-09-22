from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.decorators import action
import stripe
from django.db import transaction
from books_service import settings
from payments.models import Payment
from payments.serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


class PaymentViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin):
    queryset = Payment.objects.select_related("borrowing")
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_staff:
            return queryset
        else:
            queryset = queryset.filter(borrowing__user=self.request.user)
        return queryset

    @action(detail=False, methods=["get"], url_path="success")
    def success(self, request):
        successful_payments = Payment.objects.filter(status=Payment.PaymentStatus.PAID)
        serializer = PaymentSerializer(successful_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="cancel")
    def cancel(self, request):
        cancelled_payments = Payment.objects.filter(
            status=Payment.PaymentStatus.PENDING
        )
        serializer = PaymentSerializer(cancelled_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@transaction.atomic
def successful_payment(request, session_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        payment = Payment.objects.get(session_id=session_id)
        payment.status = Payment.PaymentStatus.PAID
        payment.save()

        return HttpResponse("Payment was successfully paid")
    else:
        return HttpResponse("Payment was not successfully paid")


def cancelled_payment(request):
    return HttpResponse("Payment was canceled. You can pay later , the session is available for only 24 hours")
