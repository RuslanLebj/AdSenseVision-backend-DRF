# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db import transaction
from django.db.models import F
from rest_framework import serializers, viewsets
from datetime import timedelta
from datetime import datetime


def time_to_timedelta(time_obj):
    return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)


def add_times(time1, time2):
    datetime1 = datetime.combine(datetime.min, time1)
    datetime2 = datetime.combine(datetime.min, time2)
    return (datetime1 + (datetime2 - datetime.min)).time()



class Camera(models.Model):
    name = models.CharField(max_length=120)
    url_address = models.CharField(max_length=80)
    connection_login = models.CharField(max_length=50)
    connection_password = models.CharField(max_length=50)
    location_address = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camera'
        # Параметры для панели администратора
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"


class CameraScreen(models.Model):
    camera = models.ForeignKey(Camera, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey('Screen', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camera_screen'
        # Параметры для панели администратора
        verbose_name = "Камера-экран"
        verbose_name_plural = "Камера-экран"


class MediaContent(models.Model):
    video = models.FileField(upload_to='videos/')  # Изменено на FileField
    name = models.CharField(max_length=120, blank=True, null=True)
    description = models.CharField(max_length=360, blank=True, null=True)
    upload_date = models.DateField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    preview = models.ImageField(upload_to='previews/', blank=True, null=True)  # Изменено на ImageFiled

    class Meta:
        managed = False
        db_table = 'media_content'
        # Параметры для панели администратора
        verbose_name = "Медиаконтент"
        verbose_name_plural = "Медиаконтент"


class Schedule(models.Model):
    queue_number = models.IntegerField()
    media_content = models.ForeignKey(MediaContent, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey('Screen', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule'
        # Параметры для панели администратора
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"


class Screen(models.Model):
    name = models.CharField(max_length=120)
    start_time = models.TimeField()
    end_time = models.TimeField()
    pause_time = models.TimeField()
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'screen'
        # Параметры для панели администратора
        verbose_name = "Экран"
        verbose_name_plural = "Экраны"


class Statistics(models.Model):
    media_content = models.ForeignKey(MediaContent, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey(Screen, models.DO_NOTHING, blank=True, null=True)
    total_viewing_time = models.TimeField()
    max_viewers_count = models.IntegerField()
    show_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statistics'
        # Параметры для панели администратора
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"


class StatisticsPerShow(models.Model):
    media_content = models.ForeignKey(MediaContent, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey(Screen, models.DO_NOTHING, blank=True, null=True)
    viewing_time = models.TimeField()
    viewers_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statistics_per_show'
        # Параметры для панели администратора
        verbose_name = "Статистика показа"
        verbose_name_plural = "Статистика показа"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with transaction.atomic():
            statistics, created = Statistics.objects.get_or_create(
                media_content=self.media_content,
                screen=self.screen,
                defaults={
                    'total_viewing_time': self.viewing_time,
                    'max_viewers_count': self.viewers_count,
                    'show_count': 1
                }
            )
            if not created:
                statistics.total_viewing_time = add_times(statistics.total_viewing_time, self.viewing_time)
                statistics.max_viewers_count = max(statistics.max_viewers_count, self.viewers_count)
                statistics.show_count = F('show_count') + 1
                statistics.save()


