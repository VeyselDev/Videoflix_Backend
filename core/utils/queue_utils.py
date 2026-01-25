from typing import Callable

from django.conf import settings
from django_rq import get_queue

from rq import Retry
from rq.job import Job


def enqueue_job(
    func: Callable[..., any],
    *args: any,
    timeout: int = 120,
    retry: int = 3,
    **kwargs: any
) -> Job:
    queue = get_queue(settings.DEFAULT_QUEUE)

    return queue.enqueue(
        func,
        *args,
        **kwargs,
        retry=Retry(max=retry),
        job_timeout=timeout,
    )