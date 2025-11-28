import os
import shutil

import django_rq
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from app_video.models import Video
from app_video.tasks import convert_video_to_hls


@receiver(post_save, sender=Video)
def auto_process_video_on_save(sender, instance, created, **kwargs):
    if created and instance.video_file:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video_to_hls, instance.id)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    main_dir = os.path.dirname(instance.id)

    if os.path.exists(main_dir):
        shutil.rmtree(main_dir, ignore_errors=True)