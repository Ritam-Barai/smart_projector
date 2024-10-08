# pdfs/management/commands/cleanup_pyc.py

import os
import shutil
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cleanup Python bytecode (*.pyc) files'

    def handle(self, *args, **options):
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pyc') or file.endswith('.pkl'):
                    os.remove(os.path.join(root, file))
                    self.stdout.write(self.style.SUCCESS(f'Deleted: {os.path.join(root, file)}'))

        return
