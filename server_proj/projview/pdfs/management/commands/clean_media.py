# filecleanup/management/commands/cleanpdfs.py
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from pdfs.models import PDF  # Import your PDF model

class Command(BaseCommand):
    help = 'Deletes PDF files from the media directory'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        pdf_directory = os.path.join(media_root)  # Adjust as per your directory structure

        # Query PDF objects and delete associated files
        pdfs = PDF.objects.all()
        PDF.objects.all().delete()
        #self.stdout.write(self.style.SUCCESS('Successfully deleted all PDF files'))
        for pdf in pdfs:
            pdf_file_path = os.path.join(pdf_directory, pdf.file.name)
            try:
                os.remove(pdf_file_path)
                self.stdout.write(self.style.SUCCESS(f"Deleted {pdf.file.name}"))
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING(f"File {pdf.file.name} not found. Skipped deletion."))

        
        return

        # Optionally, delete all PDF objects from the database
        # PDF.objects.all().delete()
