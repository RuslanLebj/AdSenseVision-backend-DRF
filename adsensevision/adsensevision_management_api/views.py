from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Camera, CameraScreen, MediaContent, Schedule, Screen, Statistics
from .serializers import MediaContentSerializer, CameraSerializer, ScreenSerializer
from rest_framework.viewsets import ModelViewSet
from django.core.files.storage import default_storage


# Create your views here.


class CameraViewSet(ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class ScreenViewSet(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class MediaContentViewSet(ModelViewSet):
    queryset = MediaContent.objects.all()
    serializer_class = MediaContentSerializer




