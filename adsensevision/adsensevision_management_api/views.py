from .models import Camera, CameraScreen, MediaContent, Schedule, Screen, Statistics
from .serializers import CameraSerializer, ScreenSerializer, CameraScreenSerializer, ScheduleSerializer, \
    MediaContentReadSerializer, MediaContentWriteSerializer, StatisticsSerializer
from rest_framework.viewsets import ModelViewSet


# Create your views here.


class CameraViewSet(ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class ScreenViewSet(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class CameraScreenViewSet(ModelViewSet):
    queryset = CameraScreen.objects.all()
    serializer_class = CameraScreenSerializer


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class StatisticsViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class MediaContentViewSet(ModelViewSet):
    queryset = MediaContent.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MediaContentWriteSerializer  # Использование сериализатора для записи
        return MediaContentReadSerializer  # Использование сериализатора для чтения
