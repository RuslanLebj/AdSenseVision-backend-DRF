from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Camera, CameraScreen, MediaContent, Schedule, Screen, Statistics
from .serializers import MediaContentSerializer, CameraSerializer, ScreenSerializer
from rest_framework.viewsets import ViewSet
# Create your views here.


# Базовый класс для ViewSet для определения поведния
class BaseViewSet(ViewSet):
    @classmethod
    def get_object(cls, pk):
        try:
            return cls.model.objects.get(pk=pk)
        except cls.model.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND


class MediaContentViewSet(BaseViewSet):
    model = MediaContent
    queryset = model.objects.all()
    serializer_class = MediaContentSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CameraViewSet(BaseViewSet):
    model = Camera
    queryset = model.objects.all()
    serializer_class = CameraSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScreenViewSet(BaseViewSet):
    model = Screen
    queryset = model.objects.all()
    serializer_class = ScreenSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
