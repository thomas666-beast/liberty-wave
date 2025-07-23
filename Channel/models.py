import uuid

from django.core.exceptions import ValidationError
from django.db import models

from LibertyWave.storage_backend import PrivateMediaStorage
from Participant.models import User

def thumbnail_upload_path(instance, filename):
    return f'thumbnails/{instance.id}/{filename}'

def validate_image_size(value):
    file_size = value.size

    if file_size > 2 * 1024 * 1024:  # 2MB in bytes
        raise ValidationError("The maximum file size that can be uploaded is 2MB")


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to=thumbnail_upload_path,
        validators=[validate_image_size],
        storage=PrivateMediaStorage(),
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
