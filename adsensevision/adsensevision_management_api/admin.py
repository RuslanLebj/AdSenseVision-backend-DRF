from django.contrib import admin
from .models import Camera, Screen, CameraScreen, MediaContent, Schedule, Statistics
# Register your models here.

admin.site.register([Camera, Screen, CameraScreen, MediaContent, Schedule, Statistics])
