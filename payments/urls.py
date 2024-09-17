from rest_framework import routers
from django.urls import path, include

from payments.views import PaymentViewSet

router = routers.DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [path("", include(router.urls))]
