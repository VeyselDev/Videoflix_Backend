from pathlib import Path
import json

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create default users from seed_data/users.json"

    SEED_FILE = Path("seed_data/users.json")
    REQUIRED_FIELDS = ["username", "email", "password"]

    def handle(self, *args, **options):
        if not self.SEED_FILE.exists():
            self.stdout.write(self.style.ERROR(f"Seed file not found: {self.SEED_FILE}"))
            return

        with self.SEED_FILE.open("r", encoding="utf-8") as f:
            users_data = json.load(f)

        for user_data in users_data:
            missing_fields = [field for field in self.REQUIRED_FIELDS if not user_data.get(field)]
            if missing_fields:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping user, missing fields: {', '.join(missing_fields)}"
                    )
                )
                continue

            username = user_data["username"]
            email = user_data["email"]
            password = user_data["password"]

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_active": True,
                }
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{username}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
