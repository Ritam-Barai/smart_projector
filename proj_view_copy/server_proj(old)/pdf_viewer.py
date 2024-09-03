import tkinter as tk
from tkinter import filedialog, simpledialog
import fitz  # PyMuPDF

class PDFViewer:
    def __init__(self, root, default_pdf_path=None):
        self.root = root
        self.root.title("PDF Viewer")

        # Main frame to hold canvas and buttons
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas to display PDF pages
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Button frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, sticky="ew")

        # Configure grid to expand canvas
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Load PDF button
        self.load_button = tk.Button(self.button_frame, text="Open PDF", command=self.load_pdf)
        self.load_button.pack(side="left", padx=5, pady=5)

        # Next page button
        self.next_button = tk.Button(self.button_frame, text="Next Page", command=self.next_page)
        self.next_button.pack(side="left", padx=5, pady=5)

        # Previous page button
        self.prev_button = tk.Button(self.button_frame, text="Previous Page", command=self.prev_page)
        self.prev_button.pack(side="left", padx=5, pady=5)

        # Text annotation button
        self.annotate_button = tk.Button(self.button_frame, text="Text Annotation", command=self.enable_text_annotation)
        self.annotate_button.pack(side="left", padx=5, pady=5)

        # Drawing button
        self.draw_button = tk.Button(self.button_frame, text="Draw", command=self.enable_drawing)
        self.draw_button.pack(side="left", padx=5, pady=5)

        # Close button
        self.close_button = tk.Button(self.button_frame, text="Close", command=root.quit)
        self.close_button.pack(side="right", padx=5, pady=5)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)

        # Initialize variables
        self.pdf_path = default_pdf_path
        self.doc = None
        self.current_page = 0
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.image = None  # Store a reference to the PhotoImage object
        self.drawing_mode = False
        self.annotation_mode = False

        # Load the default PDF if provided
        if self.pdf_path:
            self.load_pdf(self.pdf_path)

    def load_pdf(self, path=None):
        if path:
            self.pdf_path = path
        else:
            # Open file dialog to select PDF file
            self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

        if self.pdf_path:
            # Open PDF document
            self.doc = fitz.open(self.pdf_path)
            self.current_page = 0
            self.show_page()

    def show_page(self):
        # Clear canvas
        self.canvas.delete("all")

        # Load current page
        page = self.doc.load_page(self.current_page)
        pix = page.get_pixmap()

        # Create PhotoImage from Pixmap
        self.image = tk.PhotoImage(data=pix.tobytes("ppm"))

        # Display page on canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.image)

        # Update window title
        self.root.title(f"PDF Viewer - Page {self.current_page + 1}/{self.doc.page_count}")

        # Get page dimensions and resize window and canvas
        page_width, page_height = pix.width, pix.height
        self.canvas.config(width=page_width, height=page_height)
        self.root.geometry(f"{page_width}x{page_height + self.button_frame.winfo_height()}")

    def next_page(self):
        if self.doc and self.current_page < self.doc.page_count - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def enable_text_annotation(self):
        self.annotation_mode = True
        self.drawing_mode = False

    def enable_drawing(self):
        self.drawing_mode = True
        self.annotation_mode = False

    def canvas_click(self, event):
        if self.annotation_mode:
            # Start highlighting
            self.start_x = event.x
            self.start_y = event.y
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="yellow", fill="yellow", stipple="gray12")
        elif self.drawing_mode:
            self.start_draw(event)

    def canvas_drag(self, event):
        if self.annotation_mode and self.rect:
            # Update the size of the highlighted rectangle
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        elif self.drawing_mode:
            self.draw(event)

    def canvas_release(self, event):
        if self.annotation_mode and self.rect:
            # Finalize the highlighted rectangle
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            # Ask for annotation text
            text = simpledialog.askstring("Input", "Enter annotation text:")
            if text:
                self.add_text_annotation((self.start_x + event.x) / 2, min(self.start_y, event.y) - 10, text)
            self.rect = None

    def add_text_annotation(self, x, y, text):
        # Add text annotation to the canvas
        self.canvas.create_text(x, y, text=text, fill="black", anchor="n")
        # You may also add the text annotation to the PDF document using PyMuPDF here if needed

    def start_draw(self, event):
        if self.doc:
            # Record starting coordinates of drawing
            self.start_x = event.x
            self.start_y = event.y

    def draw(self, event):
        if self.doc and self.drawing_mode:
            # Draw line from starting coordinates to current mouse position
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black", width=2)

            # Update starting coordinates
            self.start_x = event.x
            self.start_y = event.y

    def run(self):
        self.root.mainloop()


