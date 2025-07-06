import uuid

from django.db import models

from Participant.models import User


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='channel_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
