from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from borrow.models import Borrow
from borrow.serializers import BorrowReadSerializer


# Create your views here.
class BorrowViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Borrow.objects.select_related('book', 'user').all()
    serializer_class = BorrowReadSerializer
