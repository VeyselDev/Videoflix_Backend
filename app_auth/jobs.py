from app_auth.services.user_service import delete_inactive_users_older_than
from core.utils.logging_utils import log_info, log_exception


def delete_inactive_users_job() -> None:
    try:
        deleted_count = delete_inactive_users_older_than(hours=24)
        log_info(f"Cleanup: Deleted {deleted_count} inactive users.")
    except Exception as e:
        log_exception(f"Failed to delete inactive users: {e}", exc_info=True)