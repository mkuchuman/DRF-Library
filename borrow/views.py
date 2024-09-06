from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrow.models import Borrow
from borrow.serializers import BorrowSerializer


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
        # Не проверенно
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

        return Response({"detail": "The book was successfully returned."})
