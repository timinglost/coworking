import os
import shutil
import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        dest = 'test_data'
        src = 'media'
        shutil.copytree(src, os.path.join(dest, src))
        sysout = sys.stdout
        sys.stdout = open(os.path.join(dest, 'test_data.json'), 'w', encoding='utf-8')
        call_command('dumpdata')
        sys.stdout = sysout
