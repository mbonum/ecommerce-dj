from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Generate random user"

    def add_argurment(self, parser):
        parser.add_argument("qty", type=int, help="How many users to add")
        parser.add_argument(
            "-a", "--admin", action="store_true", help="Define an admin account"
        )

    def handle(self, *args, **kwargs):
        qty = kwargs["qty"]
        admin = kwargs["admin"]
        for i in qty:
            email = get_random_string(10)
            p = get_random_string(10)
            if admin:
                User.objects.create_superuser(email=email, password=p)
            else:
                User.objects.create_user(email=email, password=p)
            self.stdout.write(f"User {email} account created")
