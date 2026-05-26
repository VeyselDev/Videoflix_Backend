from django.db import models


class VideoStatus(models.TextChoices):
    """
    Enumeration of processing states for a Video.

    Used to track the lifecycle of video ingestion and HLS conversion.
    """
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    CONVERTED = 'converted', 'Converted'
    FAILED = 'failed', 'Failed'