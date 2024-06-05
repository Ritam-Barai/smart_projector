from tkinter import simpledialog
import subprocess
import sys

class PDFViewerAnnotate:
    def enable_text_annotation(self):
        if self.annotation_mode:
        # If annotation mode is already active, switch it off
            self.annotation_mode = False
            self.annotate_button.config(bg="lightgray")
        else:
        # If annotation mode is not active, switch it on
            self.annotation_mode = True
            self.drawing_mode = False
            self.annotate_button.config(bg="yellow")
            self.draw_button.config(bg="lightgray")

    def enable_drawing(self):
        if self.drawing_mode:
        # If drawing mode is already active, switch it off
            self.drawing_mode = False
            self.draw_button.config(bg="lightgray")
        else:
        # If drawing mode is not active, switch it on
            self.annotation_mode = False
            self.drawing_mode = True
            self.annotate_button.config(bg="lightgray")
            self.draw_button.config(bg="yellow")

    def toggle_slideshow(self):
        if self.slideshow_process:
            self.slideshow_process = False
            self.slideshow_mode = False
            self.slideshow_button.config(bg="lightgray")
            self.q.put('STOP')
            #self.proc.wait()
            self.slide_process()
            '''
        elif self.slideshow_mode and not self.slideshow_process:
        # If slideshow is already active, switch it off
            self.slideshow_mode = False
            self.slideshow_button.config(bg="lightgray")
            self.terminate()
            self.proc = subprocess.Popen([sys.executable, 'slides.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,bufsize=1, universal_newlines=True)
            self.q.put('INIT')
            self.slide_process()
            #self.p.join()
            '''
        elif not self.slideshow_mode:
        # If slideshow is not active, switch it on
            self.slideshow_mode = True
            self.slideshow_process = True
            self.slideshow_button.config(bg="yellow") 
            #self.q.put('START')
            self.q.put('START')
            self.slide_process()
            
            #self.open_slideshow_window()  

    

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
            
    def side_panel_canvas_click(self, event):
        # Get the coordinates of the mouse click event
        x = event.x
        y = event.y
        print(self.thumb_images,self.page_number_text)
        
        # Get the scroll position
        scroll_region = self.side_panel_canvas.bbox("all")
        scroll_fraction = self.side_panel_canvas.yview()
        scroll_offset = scroll_fraction[0] * (scroll_region[3] - scroll_region[1])

        # Adjust the y coordinate based on the scroll position
        y += scroll_offset
        
        
        # Iterate through the thumbnails to determine which one was clicked
        for i, (image_id, text_id) in enumerate(self.thumbnail_items):
            image_bbox = self.side_panel_canvas.bbox(image_id)
            text_bbox = self.side_panel_canvas.bbox(text_id)
            print(image_bbox,text_bbox)
            if image_bbox is not None:
                x_start, y_start, x_end, y_end = image_bbox
                if x_start <= x <= x_end and y_start <= y <= y_end:
                    # Load the corresponding page into the main frame
                    self.current_page = i
                    self.show_page()
                    break
            if text_bbox is not None:
                x_start, y_start, x_end, y_end = text_bbox
                if x_start <= x <= x_end and y_start <= y <= y_end:
                    # Load the corresponding page into the main frame
                    self.current_page = i
                    self.show_page()
                    break
                           

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

