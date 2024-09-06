from django.urls import path, include
from rest_framework import routers

from borrow.views import BorrowViewSet

router = routers.DefaultRouter()
router.register("", BorrowViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "borrowings"
