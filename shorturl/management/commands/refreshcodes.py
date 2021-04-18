"""
https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/
"""

from django.core.management.base import BaseCommand, CommandError
from shorturl.models import ClUrl


class Command(BaseCommand):
    help = "Refreshes all short ClURLs"

    def add_arguments(self, parser):
        parser.add_argument("--items", nargs="+", type=int)

    def handle(self, *args, **options):
        return ClUrl.objects.refresh_codes(items=options["items"])
