# storage_backends.py
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class PrivateMediaStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.PRIVATE_MEDIA_ROOT
        if base_url is None:
            base_url = settings.PRIVATE_MEDIA_URL
        super().__init__(location, base_url, *args, **kwargs)
