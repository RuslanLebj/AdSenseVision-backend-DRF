from .models import Camera, CameraScreen, MediaContent, Schedule, Screen, Statistics, StatisticsPerShow
from .serializers import CameraSerializer, ScreenSerializer, CameraScreenSerializer, ScheduleSerializer, \
    MediaContentReadSerializer, MediaContentCreateSerializer, StatisticsSerializer, MediaContentUpdateSerializer, \
    StatisticsPerShowSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, Http404
import json
from django.conf import settings
import os
from urllib.parse import quote
from django.core.files import File
from django_filters import rest_framework as filters
from django.db.models import Sum, Max
from rest_framework import status
from datetime import timedelta


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


class ScheduleFilter(filters.FilterSet):
    screen = filters.NumberFilter(field_name='screen')
    media_content = filters.NumberFilter(field_name='media_content')
    queue_number = filters.NumberFilter(field_name='queue_number')

    class Meta:
        model = Schedule
        fields = ['screen', 'media_content', 'queue_number']


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ScheduleFilter


class StatisticsFilter(filters.FilterSet):
    screen = filters.NumberFilter(field_name='screen')
    media_content = filters.NumberFilter(field_name='media_content')

    class Meta:
        model = Statistics
        fields = ['screen', 'media_content']


class StatisticsViewSet(ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StatisticsFilter

    # Отправка агрегированных данных для отфильтрованного набора данных (queryset)
    @action(detail=False, methods=['get'], url_path='aggregate')
    def aggregate_statistics(self, request):
        # Фильтруем queryset согласно переданным параметрам фильтрации
        filtered_queryset = self.filter_queryset(self.get_queryset())

        # Вычисляем агрегированные данные
        # Один вызов aggregate(): Метод aggregate() вызывается один раз с тремя агрегатными функциями,
        # что уменьшает количество запросов к базе данных и увеличивает производительность.
        aggregation = filtered_queryset.aggregate(
            total_viewing_time_seconds_sum=Sum('total_viewing_time'),
            max_viewers_count_max=Max('max_viewers_count'),
            show_count_sum=Sum('show_count')
        )

        # Преобразуем секунды в формат времени, убедившись, что значение не None
        # Проверка на None и преобразование timedelta в строку
        aggregation['total_viewing_time_sum'] = str(
            aggregation['total_viewing_time_seconds_sum']
        ) if aggregation['total_viewing_time_seconds_sum'] else '00:00:00'

        # Подготавливаем и отправляем ответ
        data = {
            'total_viewing_time': aggregation['total_viewing_time_sum'],
            'max_viewers_count': aggregation['max_viewers_count_max'],
            'show_count': aggregation['show_count_sum']
        }

        return Response(data, status=status.HTTP_200_OK)


class StatisticsPerShowViewSet(ModelViewSet):
    queryset = StatisticsPerShow.objects.all()
    serializer_class = StatisticsPerShowSerializer


class MediaContentViewSet(ModelViewSet):
    queryset = MediaContent.objects.all()

    # Определяем класс сериализатора в зависимости от методов
    def get_serializer_class(self):
        if self.action in ['create']:
            return MediaContentCreateSerializer  # Использование сериализатора для записи
        if self.action in ['update', 'partial_update']:
            return MediaContentUpdateSerializer  # Использование сериализатора для обновления
        return MediaContentReadSerializer  # Использование сериализатора для чтения

    #
    # # DRF Для создания полного URL нужен доступ к схеме (http или https) и домену. В Django и DRF это обычно достигается через объект request, доступный в сериализаторе через контекст.
    #
    # # В классе ViewSet (или любом другом классе, который использует сериализаторы) метод get_serializer_context определяется для того, чтобы добавлять дополнительные данные в контекст, который затем передается в сериализатор.
    # def get_serializer_context(self):
    #     # Возвращаем контекст с объектом request
    #     return {'request': self.request}
    #
    # # Влияние Контекста на Сериализацию URL
    # # Контекст request в сериализаторе:
    # # Когда вы передаёте context в сериализатор, включая объект request, DRF использует информацию из этого запроса для формирования полных URL. Это связано с тем, что DRF рассматривает наличие объекта request в контексте как указание на то, что следует использовать абсолютные URL, поскольку информация о хосте и схеме (http или https) доступна из объекта request.
    # # Отсутствие контекста request:
    # # Когда контекст не предоставляется, DRF не имеет данных о том, какой базовый URL использовать, поэтому он генерирует относительные пути. Это происходит потому, что без контекста сериализатор не знает о базовом URL сервера и возвращает URL, который начинается непосредственно с местоположения файла в медиа-хранилище.
    #
    # # Переопределение метода update для возвращения полных данных после обновления (если в serializer fields указаны не все поля)
    # def update(self, request, *args, **kwargs):
    #     # Получаем объект, который должен быть обновлен
    #     instance = self.get_object()
    #     # Создаем сериализатор для обновления с новыми данными запроса
    #     serializer = self.get_serializer(instance, data=request.data)
    #     # Проверяем валидность данных
    #     serializer.is_valid(raise_exception=True)
    #     # Выполняем операцию обновления
    #     self.perform_update(serializer)
    #
    #     # После обновления создаем новый экземпляр сериализатора,
    #     # чтобы включить в ответ все поля объекта
    #     serializer = MediaContentReadSerializer(instance, context=self.get_serializer_context())
    #     # Возвращаем ответ с полными данными о медиаконтенте
    #     return Response(serializer.data)
    #

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


class CameraServiceDetailAPIView(APIView):

    # Возвращаем полные данные о всех камерах, чьи экраны имеют расписание
    def get(self, request):
        all_cameras_data = []  # Список для хранения данных всех камер

        # Перебор всех камер
        for camera in Camera.objects.all():
            camera_data = CameraSerializer(camera).data
            camera_screens = CameraScreen.objects.filter(camera=camera)

            screens_data = []
            camera_has_schedules = False  # Флаг наличия расписания у экранов данной камеры

            # Перебор всех экранов у камеры
            for camera_screen in camera_screens:
                screen = camera_screen.screen
                schedules = Schedule.objects.filter(screen=screen)

                if schedules.exists():  # Проверка наличия расписаний у экрана
                    camera_has_schedules = True
                    screen_data = ScreenSerializer(screen).data
                    schedules_data = ScheduleSerializer(schedules, many=True).data

                    media_contents_data = []
                    for schedule in schedules:
                        media_content = schedule.media_content
                        media_content_data = MediaContentReadSerializer(media_content).data if media_content else None
                        if media_content_data:
                            media_contents_data.append(media_content_data)

                    screen_data['schedules'] = schedules_data
                    screen_data['media_contents'] = media_contents_data
                    screens_data.append(screen_data)

            # Добавляем данные камеры только если у неё есть экраны с расписаниями
            if camera_has_schedules:
                camera_data['screens'] = screens_data
                all_cameras_data.append(camera_data)

        return Response(all_cameras_data)
