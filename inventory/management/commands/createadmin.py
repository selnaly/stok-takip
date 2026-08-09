import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Render için admin kullanıcısı oluşturur."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")
        email = os.environ.get("ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_USERNAME veya ADMIN_PASSWORD eksik."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Admin kullanıcısı oluşturuldu.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Admin kullanıcısı güncellendi.")
            )