from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaContentViewSet, CameraViewSet, ScreenViewSet

# Создание экземпляра router
router = DefaultRouter()

# Регистрация ViewSet'ов с router
router.register(r'mediacontent', MediaContentViewSet, basename='mediacontent')
router.register(r'camera', CameraViewSet, basename='camera')
router.register(r'screen', ScreenViewSet, basename='screen')

urlpatterns = [
    path('api/', include(router.urls)),
]