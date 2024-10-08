from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponseRedirect
from borrow.models import Borrow
from borrow.serializers import BorrowSerializer
from payments.helper import create_stripe_payment


# Create your views here.
class BorrowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Borrow.objects.select_related("book", "user")
    serializer_class = BorrowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)
        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        borrow = self.get_object()

        if borrow.actual_return_date:
            return Response(
                {"detail": "The book is already returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            borrow,
            data={"actual_return_date": request.data["actual_return_date"]},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if borrow.actual_return_date > borrow.expected_return_date:
            payment = create_stripe_payment(borrow)
            return HttpResponseRedirect(redirect_to=payment.session_url)
        return Response({"detail": "The book was successfully returned."})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_url = serializer.save()

        return HttpResponseRedirect(redirect_to=session_url)
