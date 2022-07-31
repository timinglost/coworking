import os
import shutil
import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_data = 'test_data/test_data.json'
        src = 'test_data/media'
        dest = 'media'
        shutil.copytree(src, dest, dirs_exist_ok=True)
        call_command('loaddata', test_data)
