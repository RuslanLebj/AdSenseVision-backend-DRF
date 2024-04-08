from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet, CameraScreenViewSet, ScreenViewSet, MediaContentViewSet, ScheduleViewSet, StatisticsViewSet
from django.conf import settings
from django.conf.urls.static import static

# Создание экземпляра router
router = DefaultRouter()

# Регистрация ViewSet'ов с router
router.register(r'camera', CameraViewSet, basename='camera')
router.register(r'screen', ScreenViewSet, basename='screen')
router.register(r'camerascreen', CameraScreenViewSet, basename='camerascreen')
router.register(r'schedule', ScheduleViewSet, basename='schedule')
router.register(r'mediacontent', MediaContentViewSet, basename='mediacontent')
router.register(r'statistics', StatisticsViewSet, basename='statistics')

urlpatterns = [
    path('api/', include(router.urls)),
]

# Регистрация медиа файлов
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
