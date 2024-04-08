from celery import shared_task
from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile
from .models import MediaContent
import os
import tempfile


@shared_task
def process_video(media_content_id):

    # Получение объекта MediaContent по ID
    media_content = MediaContent.objects.get(id=media_content_id)
    # Получение объекта File, связанного с полем content в модели MediaContent
    video_file = media_content.content

    # Загрузка видеофайла в объект VideoFileClip для обработки
    video = VideoFileClip(video_file.path)

    # Извлечение названия файла без расширения
    filename, _ = os.path.splitext(os.path.basename(video_file.name))
    media_content.name = filename

    # Извлечение продолжительности видео и сохранение ее в формате MM:SS
    media_content.duration = str(int(video.duration // 60)) + ":" + str(int(video.duration % 60))

    # Задаем время кадра для превью
    frame_time = 10

    # Открываем видеофайл
    video = VideoFileClip(video_path)

    # Создаем BytesIO объект для хранения изображения в памяти
    preview_buffer = BytesIO()
    video.save_frame(preview_buffer, t=0, withmask=True)
    preview_buffer.seek(0)  # Перемещаем указатель в начало буфера

    # Сохраняем превью из памяти в модель
    filename = os.path.splitext(os.path.basename(video_path))[0] + ".jpg"
    media_content.preview.save(filename, ContentFile(preview_buffer.read()), save=False)

    video.close()  # Закрываем файл

    # Сохранение изменений в объекте MediaContent
    media_content.save(update_fields=['name', 'duration', 'preview'])
