# pdfs/signals.py

import shutil
from django.conf import settings
from django.core.signals import request_finished
from django.dispatch import receiver
import atexit
import os
from django.core.cache import cache
from subprocess import call




@receiver(request_finished)
def cleanup_cache(sender, **kwargs):
    # Function to delete files in cache directory
    def delete_cache_files():
        try:
            cache_path = cache.cache.backend.cache_dir
            shutil.rmtree(cache_path)
        except AttributeError:
            pass

    atexit.register(delete_cache_files)


@receiver(request_finished)
def cleanup_pyc(sender, **kwargs):
    def delete_pyc_files():
        try:
            call(['python', 'manage.py', 'cleanup_pyc'])
        except Exception as e:
            print(f"Error deleting .pyc files: {e}")

    # Register the delete_media function to be called at exit
    
    
    atexit.register(delete_pyc_files)


@receiver(request_finished)
def cleanup_pdfs(sender, **kwargs):
    def delete_pdfs():
        try:
            call(['python', 'manage.py', 'cleanup_pdfs'])
        except Exception as e:
            print(f"Error deleting pdf files: {e}")

    # Register the delete_media function to be called at exit
    
    
    atexit.register(delete_pdfs)



@receiver(request_finished)
def cleanup_media(sender, **kwargs):
    # Function to delete all files in media directory
    def delete_media():
        media_root = settings.MEDIA_ROOT
        pdf_directory = os.path.join(media_root)
        try:
            call(['python', 'manage.py', 'clean_media'])
            shutil.rmtree(media_root)
            os.makedirs(media_root)  
            
            #media_pdfs_dir = os.path.join(settings.MEDIA_ROOT)
            #media_pdfs_dir = settings.MEDIA_ROOT
            #shutil.rmtree(media_pdfs_dir)
            print(f"Deleted {media_root}: Clearing out files")
        except FileNotFoundError:
            pass

    #request_finished.connect(delete_media, dispatcuph_uid='clean_media')
    atexit.register(delete_media)
