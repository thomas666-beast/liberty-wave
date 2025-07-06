import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from Channel.models import Channel
from LibertyWave.storage_backend import PrivateMediaStorage


def video_upload_path(instance, filename):
    return f'videos/{instance.id}/{filename}'

def thumbnail_upload_path(instance, filename):
    return f'thumbnails/{instance.id}/{filename}'

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # video_file = models.FileField(
    #     upload_to='videos/',
    #     validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])]
    # )
    # thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    video_file = models.FileField(
        upload_to=video_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])],
        storage=PrivateMediaStorage()  # We'll create this next
    )
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_path,
        storage=PrivateMediaStorage()
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()
