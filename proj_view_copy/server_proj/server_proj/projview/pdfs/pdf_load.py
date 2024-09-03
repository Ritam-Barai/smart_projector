# pdf_load.py
from django.http import HttpResponse
from django.views import View
import os
import io  # Import the io module
import fitz  # PyMuPDF
from multiprocessing import Process, Queue, Array
import ctypes
import tempfile
import atexit
import threading
import queue
import subprocess
import sys
from .pdf_viewer_cache import PDFViewerCache
from .pdf_viewer_slides import PDFViewerSlides
from .pdf_viewer_process import PDFViewerProcess

    
class PDFViewer(View, PDFViewerCache, PDFViewerSlides, PDFViewerProcess):  
    def __init__(self,root ):
        self.root = root
        self.page_number = 1
        self.current_page = self.page_number - 1
        self.page_height = None
        self.page_width = None
        self.total_page_number = None
        self.pdf_name = None
        self.pdf_path = None
        self.cache_path = None
        self.slideshow_active = False
        self.slideshow_process = False
        self.subprocess_active = False
        self.pointer_mode = False
        self.pointer_position = Array(ctypes.c_int, [9999, 9999]) #9999 signifies empty array

        # Instiatiate subprocess for slideshow
        self.q = queue.Queue()
        self.terminate_event = threading.Event()
        
        # Start slides.py as a subprocess
        #self.args = [f'--display={self.display}']
        self.proc = None
        #self.proc = subprocess.Popen([sys.executable, 'slides.py'] + self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,bufsize=1, universal_newlines=True)
        #atexit.register(self.proc.terminate)
        
        self.flag_condition = threading.Condition()
        self.coord_condition = threading.Condition()
        self.flag_lock = threading.Lock()
        self.slide_process()
        #self.handle_new_flag("INIT")
        # Load or create the slideshow cache file
        self.slideshow_cache_file = "cache/slideshow_cache.pkl"
        self.load_slideshow_cache()
        atexit.register(self.release_slideshow_cache)

    
    def slideshow_housekeep(self):
        if not self.slideshow_process:
            #self.pointer_mode = False
            #self.toggle_pointer()
            #self.slideshow_button.config(bg="lightgray")
            self.terminate()
            self.pause_event.clear()
            #self.new_slideshow()
            
    
    def new_slideshow(self):
        while not self.q.empty():
            try:
                self.q.get_nowait()
            except queue.Empty:
                break
        #self.args = [f'--display={self.display}']
        #print(self.display)
        self.proc = subprocess.Popen([sys.executable, 'slides.py'] , stdin=subprocess.PIPE, stdout=subprocess.PIPE,bufsize=1, universal_newlines=True)
        atexit.register(self.proc.terminate)
        
        self.handle_new_flag("INIT")
        self.slide_process()
    
    def render_pdf_page(self, pdf_name = None, page_number = None):
        self.pdf_name = pdf_name
        self.page_number = page_number
        # Ensure the page_number is an integer
        self.page_number = int(self.page_number)

        # Build the path to the PDF
        self.pdf_path = os.path.join('media', 'pdfs', self.pdf_name)
        
        # Check if the PDF file exists
        if not os.path.exists(self.pdf_path):
            return HttpResponse(status=404)

        # Open the PDF using PyMuPDF
        doc = fitz.open(self.pdf_path)
        total_pages = doc.page_count

        # Check if the requested page number is within range
        if self.page_number < 1 or self.page_number > total_pages:
            return HttpResponse(status=404)

        # Select the specified page
        page = doc.load_page(self.page_number - 1)  # PyMuPDF pages are 0-indexed
        self.total_page_number = total_pages
        self.current_page = self.page_number - 1
        # Render the page to an image
        pix = page.get_pixmap()
        page_string = pix.tobytes("ppm")
        self.page_width, self.page_height = pix.width, pix.height

        self.save_slideshow_cache(page_string)
        self.load_slideshow_cache()
        if self.slideshow_process:
            self.slideshow_process = True
            self.handle_new_flag("SHOW")
        
        # Convert the image to a format suitable for HTTP response
        img_io = io.BytesIO()
        img_io.write(pix.tobytes('png'))
        img_io.seek(0)

        # Include total pages in response headers
        response = HttpResponse(img_io, content_type='image/png')
        response['X-Total-Pages'] = total_pages
        return response
