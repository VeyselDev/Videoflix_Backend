from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from app_video.jobs import convert_video_to_hls_job
from app_video.models.video import Video

from app_video.services.video_service import delete_video_files
from core.utils.logging_utils import log_info
from core.utils.queue_utils import enqueue_job


@receiver(post_save, sender=Video)
def video_created(sender: type[Video], instance: Video, created: bool, **kwargs: any) -> None:
    """
    Signal handler triggered after a Video instance is created.

    Enqueues a background job to convert the uploaded video into HLS format.
    """
    if created:
        log_info("Signal video_created triggered for id %s", instance.pk)
        enqueue_job(convert_video_to_hls_job, instance.pk, timeout=1000)


@receiver(post_delete, sender=Video)
def video_deleted(sender: type[Video], instance: Video, **kwargs: any) -> None:
    """
    Signal handler triggered after a Video instance is deleted.

    Cleans up associated media files from storage.
    """
    log_info("Signal video_deleted triggered for id %s", instance.pk)
    delete_video_files(instance)