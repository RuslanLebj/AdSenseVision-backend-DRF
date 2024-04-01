from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaContentViewSet, CameraViewSet

# Создание экземпляра router
router = DefaultRouter()

# Регистрация ViewSet'ов с router
router.register(r'mediacontent', MediaContentViewSet, basename='mediacontent')
router.register(r'camera', CameraViewSet, basename='camera')

urlpatterns = [
    path('api/', include(router.urls)),
]