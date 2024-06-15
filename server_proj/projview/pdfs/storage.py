from django.core.files.storage import FileSystemStorage
from django.conf import settings

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        print(f"Checking availability for file: {name}")
        # If the filename already exists, delete the existing file
        if self.exists(name):
            print(f"File {name} exists, deleting...")
            self.delete(name)
            print(f"File {name} ")
        return name

# In your settings.py, you can use this storage for your file uploads

