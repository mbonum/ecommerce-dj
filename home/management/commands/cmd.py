from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    # ./manage.py cmd -h the name of the file is the name of the command
    help = "Docs command"

    def handle(self, *args, **kwargs):
        name = get_random_string(length=32)
        self.stdout.write(name)
