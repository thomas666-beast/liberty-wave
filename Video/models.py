import uuid

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from Channel.models import Channel
from LibertyWave.storage_backend import PrivateMediaStorage


def video_upload_path(instance, filename):
    return f'videos/{instance.id}/{filename}'

def thumbnail_upload_path(instance, filename):
    return f'thumbnails/{instance.id}/{filename}'


def validate_file_size(value):
    file_size = value.size

    if file_size > 100 * 1024 * 1024:  # 100MB in bytes
        raise ValidationError("The maximum file size that can be uploaded is 100MB")


def validate_image_size(value):
    file_size = value.size

    if file_size > 2 * 1024 * 1024:  # 2MB in bytes
        raise ValidationError("The maximum file size that can be uploaded is 2MB")

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_file = models.FileField(
        upload_to=video_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg']), validate_file_size],
        storage=PrivateMediaStorage()
    )
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_path,
        validators=[validate_image_size],
        storage=PrivateMediaStorage()
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()
