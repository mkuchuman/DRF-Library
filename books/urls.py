from rest_framework import routers
from django.urls import include, path

from books.views import BookViewSet

router = routers.DefaultRouter()
router.register("", BookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "books"
