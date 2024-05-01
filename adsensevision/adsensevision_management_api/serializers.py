from rest_framework import serializers
from .models import Camera, CameraScreen, MediaContent, Schedule, Screen, Statistics, StatisticsPerShow
from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile
from .models import MediaContent
import os
import tempfile
from django.utils import timezone


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class CameraScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraScreen
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'


class StatisticsSerializer(serializers.ModelSerializer):
    screen_detail = ScreenSerializer(source='screen', read_only=True)

    class Meta:
        model = Statistics
        fields = ['media_content', 'screen', 'screen_detail', 'total_viewing_time', 'max_viewers_count', 'show_count']


class StatisticsPerShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsPerShow
        fields = '__all__'


class MediaContentReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaContent
        fields = '__all__'  # Включаем все поля модели в сериализатор


    #
    # Определение дополнительных полей для полного URL видео и превью (По умолчанию возвращаются полные URL при указании контекста в serializer):
    # SerializerMethodField: Этот тип поля в сериализаторе указывает на то, что значение поля должно быть получено с помощью метода, который вы определите. Когда Django REST Framework сериализует объект, он будет искать метод в сериализаторе, который начинается с get_ за которым следует имя поля. Это означает, что:
    # Для поля video будет вызываться метод get_video.
    # Для поля preview будет вызываться метод get_preview.
    # Контекст запроса: Эти методы используют self.context.get('request') для получения текущего объекта запроса. Объект запроса используется для получения полного URL файла с помощью метода build_absolute_uri. Это полезно для создания абсолютных URL-адресов для медиафайлов, которые могут быть доступны клиентам вне сервера, где хостится ваше приложение.
    # video = serializers.SerializerMethodField()
    # preview = serializers.SerializerMethodField()
    #
    # # Метод для получения полного URL видеофайла
    # def get_video(self, obj):
    #     if obj.video:
    #         request = self.context.get('request')  # Получение объекта запроса из контекста
    #         video_url = obj.video.url  # Получение URL из модели
    #         return request.build_absolute_uri(video_url)  # Строим полный URL
    #     return None  # Возвращаем None, если видео отсутствует
    #
    # # Метод для получения полного URL файла превью
    # def get_preview(self, obj):
    #     if obj.preview:
    #         request = self.context.get('request')  # Получение объекта запроса из контекста
    #         preview_url = obj.preview.url  # Получение URL из модели
    #         return request.build_absolute_uri(preview_url)  # Строим полный URL
    #     return None  # Возвращаем None, если превью отсутствует
    #


class MediaContentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ['name', 'description']

    # Используем 'to_representation' как альтернативу переопределению метода update для ViewSet - для возвращения всех данных обьекта после обновления
    def to_representation(self, instance):
        # DRF Для создания полного URL нужен доступ к схеме (http или https) и домену. В Django и DRF это обычно достигается через объект request, доступный в сериализаторе через контекст.
        return MediaContentReadSerializer(instance, context=self.context).data
        # Влияние Контекста на Сериализацию URL
        # Контекст request в сериализаторе:
        # Когда вы передаёте context в сериализатор, включая объект request, DRF использует информацию из этого запроса для формирования полных URL. Это связано с тем, что DRF рассматривает наличие объекта request в контексте как указание на то, что следует использовать абсолютные URL, поскольку информация о хосте и схеме (http или https) доступна из объекта request.
        # Отсутствие контекста request:
        # Когда контекст не предоставляется, DRF не имеет данных о том, какой базовый URL использовать, поэтому он генерирует относительные пути. Это происходит потому, что без контекста сериализатор не знает о базовом URL сервера и возвращает URL, который начинается непосредственно с местоположения файла в медиа-хранилище.


class MediaContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ['video']  # Ограничение полей для записи

    def create(self, validated_data):
        instance = super().create(validated_data)
        # Получение объекта MediaContent по ID
        media_content = MediaContent.objects.get(id=instance.id)
        # Получение объекта File, связанного с полем content в модели MediaContent
        video_file = media_content.video

        # Загрузка видеофайла в объект VideoFileClip для обработки
        video = VideoFileClip(video_file.path)

        # Извлечение названия файла без расширения
        filename, _ = os.path.splitext(os.path.basename(video_file.name))
        media_content.name = filename

        # Установка текущей даты и времени загрузки
        media_content.upload_date = timezone.now()

        # Извлечение продолжительности видео и сохранение ее в формате MM:SS
        media_content.duration = str(int(video.duration // 60)) + ":" + str(int(video.duration % 60))

        # Задаем время кадра для превью
        frame_time = 0

        # Создаем временный файл
        fd, temp_preview_path = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)  # Закрываем файловый дескриптор

        try:
            # Сохраняем кадр во временный файл
            video.save_frame(temp_preview_path, t=frame_time)

            # Открываем и читаем временный файл для сохранения в модель
            with open(temp_preview_path, "rb") as file:
                media_content.preview.save(f"{filename}.jpg", ContentFile(file.read()), save=False)

        finally:
            video.close()  # Явно закрываем video
            os.remove(temp_preview_path)  # Удаляем временный файл

        # Сохранение изменений в объекте MediaContent
        media_content.save(update_fields=['name', 'duration', 'preview', 'upload_date'])
        return instance

