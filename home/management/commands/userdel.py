from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete user"

    def add_argurment(self, parser):
        parser.add_argument("user_id", nargs="+", type=int, help="User id")

    def handle(self, *args, **kwargs):
        users = kwargs["user_id"]
        for u_id in users:
            try:
                user = User.objects.get(pk=u_id)
                user.delete()
                self.stdout.write(f"User {user.email} account deleted")
            except User.DoesNotExist:
                self.stdout.write(f"User {user.email} does not exist")
