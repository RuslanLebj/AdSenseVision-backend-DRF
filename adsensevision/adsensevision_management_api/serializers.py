from rest_framework import serializers
from .models import Camera, CameraScreen, MediaContent, Schedule, Screen


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class CameraScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraScreen
        fields = '__all__'


class MediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'
