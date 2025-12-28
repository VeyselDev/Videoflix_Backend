from django.conf import settings
from django_rq import get_queue

from rq import Retry


def enqueue_job(func, *args, **kwargs):
    retry_attempts = 3
    job_timeout_seconds = 120
    queue = get_queue(settings.RQ_DEFAULT_QUEUE)

    return queue.enqueue(
        func,
        *args,
        **kwargs,
        retry=Retry(max=retry_attempts),
        job_timeout=job_timeout_seconds
    )