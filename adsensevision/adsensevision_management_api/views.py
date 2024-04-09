from .models import Camera, CameraScreen, MediaContent, Schedule, Screen, Statistics
from .serializers import CameraSerializer, ScreenSerializer, CameraScreenSerializer, ScheduleSerializer, \
    MediaContentReadSerializer, MediaContentWriteSerializer, StatisticsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, Http404
import json
from django.conf import settings
import os
from urllib.parse import quote
from django.core.files import File


# Create your views here.


class CameraViewSet(ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class ScreenViewSet(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer

    # Метод для загрузки или просмотра данных видеоменеджера по выбранному экрану
    @action(detail=True, methods=['get'], url_path='videomanager/(?P<mode>[^/.]+)')
    def videomanager(self, request, pk=None, mode=None):
        screen = self.get_object()
        schedules = Schedule.objects.filter(screen=screen)
        media_contents = MediaContent.objects.filter(id__in=schedules.values('media_content_id'))

        screen_data = ScreenSerializer(screen).data
        schedule_data = ScheduleSerializer(schedules, many=True).data
        media_content_data = MediaContentReadSerializer(media_contents, many=True).data

        response_data = {
            'screen': screen_data,
            'schedule': schedule_data,
            'media_content': media_content_data
        }

        if mode == 'download':
            response = HttpResponse(json.dumps(response_data), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="videomanager_data.json"'
            return response
        elif mode == 'show':
            return Response(response_data)


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

    # Определяем класс сериализатора в зависимости от методов
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MediaContentWriteSerializer  # Использование сериализатора для записи
        return MediaContentReadSerializer  # Использование сериализатора для чтения

    # Скачивание видео
    @action(detail=True, methods=['get'], url_path='video/download')
    def download_video(self, request, pk=None):
        media_content = self.get_object()
        video_file = media_content.video

        if not video_file:
            return Response({'error': 'Video file not found'}, status=404)

        file_name = video_file.name.split('/')[-1]
        response = HttpResponse(video_file, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
        return response

    # Скачивание превью
    @action(detail=True, methods=['get'], url_path='preview/download')
    def download_preview(self, request, pk=None):
        media_content = self.get_object()
        preview_file = media_content.preview

        if not preview_file:
            return Response({'error': 'Preview file not found'}, status=404)

        file_name = preview_file.name.split('/')[-1]
        response = HttpResponse(preview_file, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
        return response


