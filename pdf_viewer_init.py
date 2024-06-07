import tkinter as tk
from tkinter import filedialog, simpledialog
import tempfile
import atexit
import threading
import queue
import subprocess
import sys
from multiprocessing import Process, Queue, Array
import ctypes

class PDFViewerInit:
    def __init__(self, root, default_pdf_path=None, display = ':1.0'):
        self.root = root
        self.root.title("PDF Viewer")
        
        
        # Main frame to hold canvas and buttons
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Top navigation button frame
        self.top_button_frame = tk.Frame(self.main_frame, bg="lightgray")
        self.top_button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Button frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        
                # Side panel frame
        self.side_panel_width = 200
        self.side_panel_frame = tk.Frame(self.main_frame, bg="lightgray", width=self.side_panel_width)  # Set background color and width
        self.side_panel_frame.grid(row=1, column=1, sticky="ns")
        #self.side_panel_visible = True  # Track the visibility state of the side panel

        # Add some content to the side panel 
        self.side_label = tk.Label(self.side_panel_frame, text="Preview")
        self.side_label.pack(padx=10, pady=10)

        # Toggle button to show/hide side panel
        self.toggle_button_text = tk.StringVar(value="Hide Side Panel")
        self.toggle_button = tk.Button(self.button_frame, textvariable=self.toggle_button_text, command=self.toggle_side_panel)
        self.toggle_button.pack(side="right", padx=5, pady=5)
        
        
        # Scrollbar for side panel
        self.side_panel_scrollbar = tk.Scrollbar(self.side_panel_frame, orient="vertical")
        self.side_panel_scrollbar.pack(side="right", fill="y")

        # Canvas for side panel
        self.side_panel_canvas = tk.Canvas(self.side_panel_frame, bg="lightgrey", yscrollcommand=self.side_panel_scrollbar.set)
        self.side_panel_canvas.pack(fill="both", expand=True,padx = 20)
        
        # Configure scrollbar
        self.side_panel_scrollbar.config(command=self.side_panel_canvas.yview)

       # Canvas to display PDF pages
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.grid(row=1, column=0, sticky="nsew")
        

         # Configure grid to expand canvas and side panel
        self.main_frame.rowconfigure(1, weight=1)
        #self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)  # Fixed width for side panel
        #self.main_frame.rowconfigure(2, weight=1) 

        # Previous page button
        self.prev_button = tk.Button(self.button_frame, text="<--", command=self.prev_page)
        self.prev_button.pack(side="left", padx=5, pady=5)
        
        # Next page button
        self.next_button = tk.Button(self.button_frame, text="-->", command=self.next_page)
        self.next_button.pack(side="left", padx=25, pady=5)


        # Text annotation button
        self.annotate_button = tk.Button(self.button_frame, text="Text Annotation", command=self.enable_text_annotation)
        self.annotate_button.pack(side="left", padx=25, pady=5)

        # Drawing button
        self.draw_button = tk.Button(self.button_frame, text="Draw", command=self.enable_drawing)
        self.draw_button.pack(side="left", padx=5, pady=5)

        # Load PDF button
        self.load_button = tk.Button(self.top_button_frame, text="Open PDF", command=self.load_pdf)
        self.load_button.pack(side="left", padx=5, pady=5)

        # Close button
        self.close_button = tk.Button(self.top_button_frame, text="Close", command=root.quit)
        self.close_button.pack(side="right", padx=5, pady=5)

        # Open Slideshow Button
        self.slideshow_button = tk.Button(self.top_button_frame, text="Slideshow", command=self.toggle_slideshow)
        self.slideshow_button.pack(side="left", padx=20, pady=5)

        # Pointer Button
        self.pointer_button = tk.Button(self.top_button_frame, text="Pointer", command=self.toggle_pointer)
        self.pointer_button.pack(side="left", padx=5, pady=5)
        self.pointer_button.config(state=tk.DISABLED)


        # Bind mouse events
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)
        
        # Bind click events to each page number text item
        self.side_panel_canvas.bind("<Button-1>", self.side_panel_canvas_click)
        
        # Create a temporary directory to store thumbnail images
        self.temp_dir = tempfile.mkdtemp()
        atexit.register(self.cleanup_temp_dir)
        
        self.thumb_images = []  # Store PhotoImage objects to prevent them from being garbage collected
        self.page_number_text = []
        self.thumbnail_items = []
        self.system_cache = []
        
        # Load or create the thumbnail cache file
        self.thumbnail_cache_file = "thumbnail_cache.pkl"
        self.load_thumbnail_cache()
        atexit.register(self.release_thumbnail_cache)

        # Load or create the slideshow cache file
        self.slideshow_cache_file = "slideshow_cache.pkl"
        self.load_slideshow_cache()
        atexit.register(self.release_slideshow_cache)

        # Initialize variables
        self.pdf_path = default_pdf_path
        self.doc = None
        self.current_page = 0
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.image = None  # Store a reference to the PhotoImage object
        self.output = None
        self.proc = None
        self.pause_event = None
        self.drawing_mode = False
        self.annotation_mode = False
        
        self.slideshow_active = False
        self.pointer_mode = False
        self.slideshow_process = False
        self.side_panel_visible = True
        self.output_flag = False
        #self.current_highlight = None  # Store the current highlighted thumbnail

        #Instatiate pointer position
        self.pointer_position = Array(ctypes.c_int, [9999, 9999]) #9999 signifies empty array
        self.canvas.bind("<Motion>",  self.track_mouse)

        # Instiatiate subprocess for slideshow
        self.q = queue.Queue()
        self.terminate_event = threading.Event()
        
        # Start slides.py as a subprocess
        self.args = [f'--display={display}']
        self.proc = subprocess.Popen([sys.executable, 'slides.py'] + self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,bufsize=1, universal_newlines=True)
        atexit.register(self.proc.terminate)
        
        self.flag_condition = threading.Condition()
        self.coord_condition = threading.Condition()
        self.flag_lock = threading.Lock()
        self.slide_process()
        #self.handle_new_flag("INIT")
        


        
        # Load the default PDF if provided
        if self.pdf_path:
            self.load_pdf(self.pdf_path)


