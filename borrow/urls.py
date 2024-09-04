from django.urls import path

from borrow.views import BorrowViewSet

urlpatterns = [
    path("", BorrowViewSet.as_view({'get': 'list'}), name="borrow-list"),
    path("<int:pk>/", BorrowViewSet.as_view({'get': 'retrieve'}), name="borrow-detail"),
]

app_name = "borrowings"
