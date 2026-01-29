from django.db import models


class VideoStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    CONVERTED = 'converted', 'Converted'
    FAILED = 'failed', 'Failed'