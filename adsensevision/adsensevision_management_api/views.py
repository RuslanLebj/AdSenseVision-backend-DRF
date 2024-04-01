from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Analytics, Camera, CameraScreen, MediaContent, Schedule, Screen
from .serializers import MediaContentSerializer, CameraSerializer, ScreenSerializer
from rest_framework.viewsets import ViewSet
# Create your views here.


class MediaContentViewSet(ViewSet):
    def list(self, request):
        queryset = MediaContent.objects.all()
        serializer = MediaContentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = MediaContentSerializer(instance)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return MediaContent.objects.get(pk=pk)
        except MediaContent.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND


class CameraViewSet(ViewSet):
    def list(self, request):
        queryset = Camera.objects.all()
        serializer = CameraSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = CameraSerializer(instance)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Camera.objects.get(pk=pk)
        except Camera.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
