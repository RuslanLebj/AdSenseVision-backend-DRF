from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Camera, CameraScreen, MediaContent, Schedule, Screen, Statistics
from .serializers import CameraSerializer, ScreenSerializer, MediaContentReadSerializer, MediaContentWriteSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.core.files.storage import default_storage
from rest_framework import generics, mixins, views
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import FileUploadParser
from django.conf import settings


# Create your views here.


class CameraViewSet(ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class ScreenViewSet(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class MediaContentViewSet(ModelViewSet):
    queryset = MediaContent.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MediaContentWriteSerializer  # Использование сериализатора для записи
        return MediaContentReadSerializer  # Использование сериализатора для чтения
