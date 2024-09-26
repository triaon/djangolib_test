from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibraryViewSet, BookViewSet

router = DefaultRouter()
router.register(r'libraries', LibraryViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
