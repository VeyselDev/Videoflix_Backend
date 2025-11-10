from datetime import datetime, timezone

import django_rq

def schedule_delete_inactive_users():
    scheduler = django_rq.get_scheduler('default')

    existing_jobs = [job.func for job in scheduler.get_jobs()]
    if 'app_authentication.tasks.delete_inactive_users' not in existing_jobs:
        scheduler.schedule(
            scheduled_time=datetime.now(timezone.utc),
            func='app_authentication.tasks.delete_inactive_users',
            interval=3600,
            repeat=None
        )
