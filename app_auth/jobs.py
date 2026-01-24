import logging

from app_auth.services.user_service import delete_inactive_users_older_than

logger = logging.getLogger(__name__)

def delete_inactive_users_job() -> None:
    try:
        deleted_count = delete_inactive_users_older_than(hours=24)
        logger.info(f"Cleanup: Deleted {deleted_count} inactive users.")
    except Exception as e:
        logger.error(f"Failed to delete inactive users: {e}", exc_info=True)