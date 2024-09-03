# myapp/management/commands/cleanup_books.py

from django.core.management.base import BaseCommand
from pdfs.models import PDF

class Command(BaseCommand):
    help = 'Deletes all pdfs from the database'

    def handle(self, *args, **options):
        PDF.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all pdfs'))

        return
#print(f"Deleted all files in {media_root} successfully.")