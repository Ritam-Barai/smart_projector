import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from tkinter.font import Font
import io
from pdf_viewer_cache import PDFViewerCache
import sys
import threading
import queue
import time
import select

class PDFViewerSlides:

    def __init__(self, root, default_pdf_path=None):
        self.root = root
        self.root.title("Slideshow Viewer")
        self.root.withdraw()

        # Create a new window
        self.slideshow_window = tk.Frame(root)
        self.slideshow_window.pack(fill="both", expand=True)

        self.slideshow_status = True
        self.slide_flag = False
        self.flag = None
        self.slideshow_cache_file = "slideshow_cache.pkl"
        self.flag_queue = queue.Queue()
        self.pause_event = threading.Event()
        self.pause_event.set()

        
        print("Slideshow Viewer Initialized")

        if self.slide_flag:
            #self.root.after(0,lambda : self.load_slide(self.pause_event))
             self.root.after(0, self.load_slide)
        
    
            
            
        

        

    
    def open_slideshow_window(self):
        
        
        # Make the window full screen
        self.root.deiconify()
        self.root.attributes('-fullscreen', True)
        #self.root.overrideredirect(True)

        


        # Create a canvas in the new window
        self.slideshow_canvas = tk.Canvas(self.slideshow_window, bg='black')
        self.slideshow_canvas.pack(fill="both", expand=True)

        # Get the fullscreen dimensions
        self.fullscreen_width = self.slideshow_window.winfo_screenwidth()
        self.fullscreen_height = self.slideshow_window.winfo_screenheight()
        print(self.fullscreen_width,self.fullscreen_height)

        # Set the pointer status
        self.pointer_status = False
        self.scaled_x, self.scaled_y = 0, 0

        # Bind the window close event to the exit_slideshow function
        self.root.protocol("WM_DELETE_WINDOW", self.exit_slideshow)
        # In open_slideshow_window:
        self.slideshow_window.focus_set()
        self.slideshow_window.bind("<Escape>", self.exit_slideshow)
        self.slideshow_window.bind("<Left>",  lambda event: self.change_slide('<Left>', event))
        self.slideshow_window.bind("<Right>",  lambda event: self.change_slide('<Right>', event))
        
        

    def change_slide(self,key, event ):
        #print(key)
        self.key_strokes_output(key)

    def key_strokes_output(self,key_stroke):
        #print(key_stroke)
        sys.stdout.write(f'{key_stroke}\n')
        sys.stdout.flush()

    def exit_slideshow(self,event = None):
        print("Slideshow exit")
        self.slideshow_status = False
        self.key_strokes_output('<Escape>')
        self.root.attributes('-fullscreen', False)
        self.root.destroy()
        #self.toggle_slideshow()

    def show_slide_page(self):
        PDFViewerCache.load_slideshow_cache(self)
        self.slideshow_canvas.delete("all")
        #print(self.slideshow_cache)
        if self.slideshow_status:
            self.slide_data = self.slideshow_cache
            

            # Get the page dimensions
            self.page_width = self.slide_data['page_width']
            self.page_height = self.slide_data['page_height']
            self.curr_page = self.slide_data['current_page']
            self.total_pages = self.slide_data['total_pages']

            # Calculate the scale factor
            self.scale_factor = min(self.fullscreen_width / self.page_width, self.fullscreen_height / self.page_height)
            print(self.scale_factor,self.page_width ,self.page_height)

            # Update the canvas size 
            self.slideshow_canvas.config(width=int(self.page_width * self.scale_factor), height=int(self.page_height * self.scale_factor))
            self.slideshow_window.config(width=int(self.page_width * self.scale_factor), height=int(self.page_height * self.scale_factor))
            self.slideshow_canvas.update()
            self.slideshow_window.update()

            
            
            self.pil_image = Image.open(io.BytesIO(self.slide_data['photoimage']))
            # Resize the image
            resized_image = self.pil_image.resize((int(self.page_width * self.scale_factor),int(self.page_height * self.scale_factor)), Image.BICUBIC)
            enhancer = ImageEnhance.Sharpness(resized_image)
            resized_image = enhancer.enhance(20.0)  # Increase sharpness by a factor of 2.0

            
            self.slide_image = ImageTk.PhotoImage(resized_image)
            print(self.slide_image,(self.fullscreen_width - self.slide_image.width()) //2)
            self.slideshow_canvas.create_image((self.fullscreen_width - self.slide_image.width()) //2, 0, anchor="nw", image=self.slide_image)
            print(self.slide_image.width(),self.slide_image.height())
            self.page_number_text()
            self.pointer = self.slideshow_canvas.create_oval(self.scaled_x + (self.fullscreen_width - self.slide_image.width()) //2 , self.scaled_y, self.scaled_x + 20 + (self.fullscreen_width - self.slide_image.width()) //2, self.scaled_y + 20, fill="red", outline="red")
            self.toggle_pointer()
            

            


    def page_number_text(self):
        margin = 10
        width, height = 100, 50
        radius = 20
        
        x1 = self.fullscreen_width - width - margin
        y1 = self.fullscreen_height - height - margin
        x2 = self.fullscreen_width - margin
        y2 = self.fullscreen_height - margin

        def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
            points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

            return self.slideshow_canvas.create_polygon(points, **kwargs, smooth=True)

        self.id = create_rounded_rectangle(self, x1, y1, x2, y2, radius=radius, fill='grey', outline='black')    

        self.text_id = self.slideshow_canvas.create_text((x1 + x2) // 2 - 5, (y1 + y2) // 2, text=f" {self.curr_page+1}|{self.total_pages}", font=Font(size=15,weight = 'bold'))
        
    def toggle_pointer(self):

        if self.pointer_status:
            self.slideshow_canvas.itemconfig(self.pointer, state='normal')
        else:
            self.slideshow_canvas.itemconfig(self.pointer, state='hidden')

        



    def handle_flag(self,flag = None,ready = False):
        
        self.flag_queue.put(flag)
        self.ready = ready

        self.pause_event.set()
        
        #ready = sys.stdin in select.select([sys.stdin], [], [])[0]
        #print(self.ready)
        '''
        self.flag_thread = threading.Thread(target=self.flag_handler)
        self.flag_thread.daemon = True
        self.flag_thread.start()
        self.flag_thread.join()
        '''

        #if self.slide_flag:
        
        self.flag_handler()    



    def flag_handler(self):

            
        self.flag = self.flag_queue.get()
        #print(self.flag)
        #self.slide_flag = False
                
                #print(ready)
        if self.flag == 'START':
            print('STARTING_SLIDESHOW')
            
            self.slide_flag = True
            self.pause_event.set()
            #self.open_slideshow_window()
            #self.show_slide_page()
            #self.root.after(0,self.open_slideshow_window())
            #self.root.after(0,self.show_slide_page())
            
        elif self.flag == 'SHOW':
            print('DISPLAYING_SLIDE')
            
            self.slide_flag = True
            self.pause_event.set()
            #self.show_slide_page()

        elif self.flag == 'STOP':
            print('STOPPING_SLIDESHOW')
            self.slide_flag = True
            self.pause_event.set()
            #self.exit_slideshow()

        elif self.flag == 'INIT':
            print('PREPARING_SLIDESHOW')
            if self.ready:
                self.pause_event.set()
                self.slide_flag = False    
                        
            else:
                self.pause_event.wait()
                self.slide_flag = False

        elif self.flag == 'POINT':
            print('TOGGLING POINTER')
            self.slide_flag = True
            self.pause_event.set()   

        else:    
            print(f'UNKNOWN_FLAG: {self.flag}')
            self.slide_flag = False

        #self.root.after(0,self.load_slide(self.pause_event))
        self.root.after(0, self.load_slide)
        
    def read_input(self):
        ready = sys.stdin in select.select([sys.stdin], [], [])[0]
        if ready:
            line = sys.stdin.readline().strip()
            if line:
                parts = line.split()  # Split the line into x and y
                #print(len(parts))
                if len(parts) == 1:
                    self.handle_flag(parts[0],ready) 
                else:
                    x = int(parts[0])  # Convert x & y to an integer
                    y = int(parts[1]) 
                    self.update_pointer(x,y)   

    def update_pointer(self,x,y):
        self.scaled_x, self.scaled_y = self.map_coord(x,y)
        self.slideshow_canvas.coords(self.pointer, self.scaled_x + (self.fullscreen_width - self.slide_image.width()) //2 , self.scaled_y, self.scaled_x + 20 + (self.fullscreen_width - self.slide_image.width()) //2, self.scaled_y + 20)

    def map_coord(self,x,y):
        x_scale = self.slide_image.width() / self.page_width
        y_scale = self.slide_image.height() / self.page_height

        mapped_x = x * x_scale
        mapped_y = y * y_scale

        return int(mapped_x),int(mapped_y)
    '''
    def load_slide(self,event):
        while True:    
            event.wait()
            print(self.slide_flag)
            if self.slide_flag:
                if self.flag == 'START':
                    #time.sleep(0)
                    #self.open_slideshow_window()
                    #self.handle_flag('INIT',True)
                    #self.show_slide_page()
                    self.root.after(0,self.open_slideshow_window())
                    self.root.after(0,self.show_slide_page())
                    self.run()

                elif self.flag == 'SHOW':
                
                
                    time.sleep(0)
                    self.show_slide_page()
                    #self.root.mainloop()
                
                elif self.flag == 'STOP':
                    self.exit_slideshow()

            
            self.slide_flag = False
            event.clear()
    '''
    def load_slide(self):
    # Check if the event is set
        if threading.current_thread().getName() != 'MainThread':
            return
        if self.pause_event.is_set():
        # Print the current slide flag
            print(threading.current_thread().getName(),self.slide_flag)

            if self.slide_flag:
                if self.flag == 'START':
                    self.open_slideshow_window()
                    self.show_slide_page()
                    self.key_strokes_output('LOAD')
                    # Start the slideshow
                    

                elif self.flag == 'SHOW':
                    self.show_slide_page()

                elif self.flag == 'STOP':
                    self.exit_slideshow()

                elif self.flag == 'POINT':
                    self.pointer_status = not self.pointer_status
                    self.toggle_pointer()

                # Reset the slide flag
            self.slide_flag = False

            # Clear the event
            self.pause_event.clear()        