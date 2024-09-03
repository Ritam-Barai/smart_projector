from django.core.files.storage import FileSystemStorage
from django.conf import settings

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        print(f"Checking availability for file: {name}")
        # If the filename already exists, delete the existing file
        if self.exists(name):
            print(f"File {name} exists, deleting...")
            try:
                self.delete(name)
                print(f"File {name} deleted successfully.")
            except Exception as e:
                print(f"Failed to delete {name}: {e}")
        return name

# In your settings.py, you can use this storage for your file uploads

