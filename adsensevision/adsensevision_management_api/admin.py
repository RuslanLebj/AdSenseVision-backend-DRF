from django.contrib import admin
from .models import Analytics, Camera, Screen, CameraScreen, MediaContent, Schedule
# Register your models here.

admin.site.register([Analytics, Camera, Screen, CameraScreen, MediaContent, Schedule])