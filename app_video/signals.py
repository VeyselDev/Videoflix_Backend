import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from app_video.models import Video
from app_video.services.video_service import VideoService
from app_video.tasks import convert_video_to_hls
from core.utils.queue_utils import enqueue_job

logger: logging.Logger = logging.getLogger(__name__)
video_service: VideoService = VideoService()

@receiver(post_save, sender=Video)
def video_created(sender: type[Video], instance: Video, created: bool, **kwargs: any) -> None:
    if created:
        logger.info("Signal video_created triggered for id %s", instance.pk)
        enqueue_job(convert_video_to_hls, instance.pk)


@receiver(post_delete, sender=Video)
def video_deleted(sender: type[Video], instance: Video, **kwargs: any) -> None:
    logger.info("Signal video_deleted triggered for id %s", instance.pk)
    video_service.delete_video_files(instance)