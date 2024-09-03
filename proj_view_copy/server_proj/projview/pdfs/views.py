# pdfs/views.py

from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import PDF
from .forms import PDFForm
from subprocess import call
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db import transaction
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from .pdf_load import PDFViewer

#from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image
import logging
import shutil
import os
import signal 
import subprocess
import fitz
import re
import tkinter as tk

logger = logging.getLogger(__name__)
root = tk.Tk()
root.withdraw()

viewer = PDFViewer(root)
#viewer.run()

def index(request):
    return render(request, 'pdfs/index.html')

def pdf_viewer(request):
    return render(request, 'pdfs/viewer.html')


def render_pdf_page_view(request, pdf_name, page_number):
    
    return viewer.render_pdf_page(pdf_name, page_number)
'''
def render_pdf_page(request, pdf_name, page_number):
    # Ensure the page_number is an integer
    page_number = int(page_number)

    # Build the path to the PDF
    pdf_path = os.path.join('media', 'pdfs', pdf_name)
    
    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        return HttpResponse(status=404)

    # Open the PDF using PyMuPDF
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count

    # Check if the requested page number is within range
    if page_number < 1 or page_number > total_pages:
        return HttpResponse(status=404)

    # Select the specified page
    page = doc.load_page(page_number - 1)  # PyMuPDF pages are 0-indexed

    # Render the page to an image
    pix = page.get_pixmap()
    
    # Convert the image to a format suitable for HTTP response
    img_io = BytesIO()
    img_io.write(pix.tobytes('png'))
    img_io.seek(0)

    # Include total pages in response headers
    response = HttpResponse(img_io, content_type='image/png')
    response['X-Total-Pages'] = total_pages
    return response
'''
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

@csrf_exempt  # Exempt from CSRF verification
def log_tab_event(request):
    if request.method == 'POST':
        '''
        event = request.POST.get('event', '')
        if event:
            if event == 'PDF viewer is inactive':
                print("PDF viewer is inactive")
            elif event == 'PDF viewer is active':
                print("PDF viewer is active")
            elif event == 'PDF viewer loaded':
                print("PDF viewer loaded")
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'No event data'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    '''
        # Process the data from request.body
        data = request.POST.get('event', 'No event message')
        
        # Log the message or perform other actions
        print(f'Log Message: {data}')
        
        if( data == 'PDF viewer loaded'):
            if( viewer.subprocess_active == False):
                viewer.subprocess_active = True
                viewer.new_slideshow()
        elif( data == 'PDF viewer is inactive'):
            viewer.slideshow_active = False
            viewer.slideshow_process = False
            viewer.terminate()
        elif( data == 'Slideshow Active' and not viewer.slideshow_process):
            viewer.slideshow_active = True
            viewer.slideshow_process = True
            viewer.handle_new_flag("START")
        elif( data == 'Slideshow Inactive' and viewer.slideshow_process):
            viewer.slideshow_active = False
            viewer.slideshow_process = False
            viewer.handle_new_flag("STOP")
        elif( data == 'PDF viewer is active' and viewer.slideshow_active):
            viewer.handle_new_flag("SHOW")
        elif( data == 'Tracking started' and viewer.slideshow_active):
            viewer.pointer_mode = True
            viewer.handle_new_flag("POINT")
            if( data[:12] == 'Coordinates:'):
                extract_coordinates(data[13:])
        elif( data == 'Tracking stopped'):
            viewer.pointer_mode = False

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def extract_coordinates(data):
    # Regular expression to find x and y values
    pattern = r"X=(\d+), Y=(\d+)"
    match = re.search(pattern, data)
    
    if match:
        # Extract x and y values
        x = int(match.group(1))
        y = int(match.group(2))
        
        # Assign to pointer_position array
        viewer.pointer_position = [x, y]
        
    else:
        # Handle case where pattern is not found
        raise ValueError("Coordinates not found in the data string")

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
