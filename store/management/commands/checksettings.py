from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check Django settings'

    def handle(self, *args, **kwargs):
        self.stdout.write(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")
