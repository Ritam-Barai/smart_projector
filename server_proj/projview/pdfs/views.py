# pdfs/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import PDF
from .forms import PDFForm
from subprocess import call
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db import transaction
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
import shutil
import os
import signal 
import subprocess

def index(request):
    return render(request, 'pdfs/index.html')

'''
def upload_pdf(request):
    if request.method == 'POST':

        #request.session.setdefault('key', 'default_value')
        form = PDFForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.cleaned_data['file']
            #session = Session.objects.get(session_key=request.session.session_key)
            # Create a new PDF object and associate it with the current session
            #pdf = PDF.objects.create(file=form.cleaned_data['file'])
            #pdf = form.save()
            if not PDF.objects.filter(file=file.name).exists():
                # Create a new PDF object and associate it with the current session
                pdf = PDF.objects.create(file=file)
                return JsonResponse({
                    'pdfs': [
                        {'name': pdf.file.name, 'url': pdf.file.url}
                    ]
                })
            else:
                return JsonResponse({'error': 'File already exists'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
'''

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.cleaned_data['file']
            file_name = file.name.lower()  # Case-insensitive check
            print(f"File name: {file_name}")
            #file_name = file.name

            # Check if a PDF with the same name already exists (case-insensitive)
            if not PDF.objects.filter(file__iexact=file_name).exists():
                # Create a new PDF object and save it
                pdf = form.save()
                return JsonResponse({
                    'pdfs': [
                        {'name': pdf.file.name, 'url': pdf.file.url}
                    ]
                })
            else:
                return JsonResponse({'error': 'File with this name already exists'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def list_pdfs(request):
    pdfs = PDF.objects.all()
    pdfs_list = [{'name': pdf.file.name, 'url': pdf.file.url} for pdf in pdfs]
    return JsonResponse({'pdfs': pdfs_list})

def proj_IP(request):
    
    return render(request, 'index.html')

@csrf_exempt
def stop_server(request):
    if request.method == 'POST':
        '''
        try:
            # Replace 'path/to/stop_server.sh' with the actual path to your script
            subprocess.run(['bash', f'{settings.BASE_DIR}/kill_server.sh'], check=True)
            return JsonResponse({'status': 'Server stopping...'})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': 'Failed to stop server'}, status=500)
        '''
        if cache.get('stop_server_subprocess_running'):
            return JsonResponse({'error': 'Subprocess is already running.'}, status=400)

        # Set the flag to indicate the subprocess is running
        cache.set('stop_server_subprocess_running', True, timeout=60)  # Timeout in seconds

        script_path = f'{settings.BASE_DIR}/kill_server.sh'
        
    try:
        proc = subprocess.Popen(['bash', script_path], preexec_fn=os.setsid)
        response = {'status': 'Server stopping...','code': 200}
        return JsonResponse(response)
    except subprocess.CalledProcessError:
        logger.exception("Failed to stop server due to subprocess error.")
        response = {'error': 'Failed to stop server due to subprocess error.', 'code': 500}
    except FileNotFoundError:
        logger.exception("Script file not found.")
        response = {'error': 'Script file not found.', 'code': 500}
    except subprocess.TimeoutExpired:
        logger.exception("Stopping server subprocess timed out.")
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        response = {'error': 'Stopping server subprocess timed out.', 'code': 500}
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
        response = {'error': f'An unexpected error occurred: {str(e)}', 'code': 500}
    finally:
            # Clear the flag once the subprocess completes
            cache.delete('stop_server_subprocess_running')
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def health_check(request):
    return JsonResponse({'status': 'ok'})

@require_POST
def delete_media_files(request):
    if request.method == 'POST':
        # Example: Delete all files in MEDIA_ROOT
        media_root = settings.MEDIA_ROOT
        try:
            #shutil.rmtree(media_root)
            #os.makedirs(media_root)  # Recreate the directory if needed
            #self.stdout.write(self.style.SUCCESS('Successfully deleted all objects'))
            #cache_path = cache.cache.backend.cache_dir
            #shutil.rmtree(cache_path)
            #deleted_count, _ = PDF.objects.all.delete
            '''
            with transaction.atomic():
            #call(['python3', 'manage.py', 'cleanup_pdfs'])
                call(['python', 'manage.py', 'flush', '--noinput'])
                deleted_count, _ = PDF.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} records from MyModel'))
                #print(f"Deleted {deleted_count} PDF objects successfully.")
                logger.info(f"Deleted {deleted_count} PDF objects successfully.")
                
            transaction.commit()
            '''
            return JsonResponse({'success': True,'deleted count': deleted_count})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
