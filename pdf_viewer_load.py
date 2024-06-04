import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import os
import tempfile
import shutil  # Import shutil module for file operations
import atexit
import pickle

class PDFViewerLoad:

    def load_pdf(self, path=None):
        
        if path:
            self.pdf_path = path
        else:
            # Open file dialog to select PDF file
            self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            self.clear_cache_file()
            print(self.thumbnail_cache)

        if self.pdf_path:
            # Open PDF document
            self.doc = fitz.open(self.pdf_path)
            print(self.thumbnail_cache)
            
            self.clear_temp_directory()
            print(os.listdir(self.temp_dir))
            self.current_page = 0
            self.show_page()
            self.show_side_panel()  # Display thumbnails in the side panel

    def show_page(self):
        # Clear canvas
        self.canvas.delete("all")

        # Load current page
        page = self.doc.load_page(self.current_page)
        pix = page.get_pixmap()

        # Create PhotoImage from Pixmap
        self.image = tk.PhotoImage(data=pix.tobytes("ppm"))
        print("Page",self.image)

        # Display page on canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.image)

        # Update window title
        self.root.title(f"PDF Viewer - Page {self.current_page + 1}/{self.doc.page_count}")

        # Get page dimensions and resize window and canvas
        self.page_width, self.page_height = pix.width, pix.height
        self.canvas.config(width=self.page_width, height=self.page_height)
        self.root.geometry(f"{self.page_width+self.side_panel_width+10}x{self.page_height + self.button_frame.winfo_height()}")
        
        # Update thumbnail border
        #self.update_thumbnail_border()
        
        
    def next_page(self):
        if self.doc and self.current_page < self.doc.page_count - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page()
            
    def toggle_side_panel(self):
        '''
        if self.side_panel_frame.winfo_x() < 0:
            # Show side panel
            self.side_panel_frame.place(x=0, y=0)
            self.toggle_button_text.set("Hide Side Panel")
        else:
            # Hide side panel
            self.side_panel_frame.place(x=-self.side_panel_width, y=0)
            self.toggle_button_text.set("Show Side Panel")
            
        '''    
        if self.side_panel_visible:
            self.side_panel_frame.grid_remove()  # Hide the side panel
            self.toggle_button_text.set("Show Side Panel")
            self.side_panel_width = 0
            self.root.geometry(f"{self.page_width+self.side_panel_width+10}x{self.page_height + self.button_frame.winfo_height()}")
        else:
            self.side_panel_frame.grid()  # Show the side panel
            self.toggle_button_text.set("Hide Side Panel")
            self.side_panel_width = 200
            self.root.geometry(f"{self.page_width+self.side_panel_width+10}x{self.page_height + self.button_frame.winfo_height()}")
            self.show_side_panel()  # Display thumbnails in the side panel
        self.side_panel_visible = not self.side_panel_visible
        
            

    def render_page_to_png(self,page, width, temp_file):
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1).prescale(width / page.rect.width, width / page.rect.width))
        #print(pix.size)
        pix.pil_save(self.temp_file)
        #print(self.temp_file)
        pix = None  # Release the pixmap

    def show_side_panel(self):
        # Clear side panel canvas
        self.side_panel_canvas.delete("all")
        '''
        self.thumb_images = []  # Store PhotoImage objects to prevent them from being garbage collected
        self.page_number_text = []
        self.thumbnail_items = []
        '''
        self.thumb_images.clear()  # Store PhotoImage objects to prevent them from being garbage collected
        self.page_number_text.clear()
        self.thumbnail_items.clear()
        self.system_cache.clear()
        #self.load_thumbnail_cache()
        #self.image_data.clear()
        
            
        try:
            
            # If thumbnail cache is available, use it
            if self.thumbnail_cache:
                for index,self.image_data in enumerate(self.thumbnail_cache):
                    self.thumb_image = tk.PhotoImage(data=self.image_data["photoimage"])
                    #print("Image",self.thumb_image.height())
                    self.thumb_images.append(self.thumb_image)
                    #self.thumb_images[index] = self.thumb_image
                    
                    page_number_texts = self.image_data["page_number_text"]
                    self.page_number_text.append(page_number_texts)
                    
                    #print(self.thumb_images[index],index,self.page_number_text[index])
                    image_id = self.side_panel_canvas.create_image(self.image_data["x"], self.image_data["y"], anchor="nw", image=self.thumb_images[index])
                    text_id = self.side_panel_canvas.create_text(self.image_data["x"] + self.thumb_images[index].width() // 2, self.image_data["y"] + self.thumb_images[index].height() + 5, anchor="n", text=page_number_texts)
                    self.thumbnail_items.append((image_id, text_id))
                print("Running from cache")
                #print(self.thumb_images)
                    
            else:
            
                # Display thumbnails of all pages
                y_offset = 0
                width = 150
                padding_x = 20        
                for i in range(self.doc.page_count):
                    page = self.doc.load_page(i)
                    '''
                pix = page.get_pixmap(matrix=fitz.Matrix(1, 1).prescale(width / page.rect.width, width / page.rect.width))
                thumb_image = tk.PhotoImage(data=pix.tobytes("ppm"))
                thumb_images.append(thumb_image)
                print(thumb_images)
                    '''
            # Render the page to a temporary PNG file with the desired dimensions 
                    self.temp_file = os.path.join(self.temp_dir, f"page_{i}.png")
                    self.render_page_to_png(page, width, self.temp_file)  # Set thumbnail width to 150 pixels
                    '''
                if os.path.exists(self.temp_file):
                    print(f"The file {self.temp_file} exists.")
                else:
                    print(f"The file {self.temp_file} does not exist.")'''

        # Create PhotoImage from the rendered PNG file
                    self.thumb_image = tk.PhotoImage(file=self.temp_file)
                    self.thumb_images.append(self.thumb_image)  # Keep the PhotoImage in memory
                #print(self.thumb_image,self.image.width(),self.thumb_image.height())
                    self.page_number_text.append(str(i + 1))
                    self.system_cache.append((self.temp_file,self.page_number_text[i]))

        # Display thumbnail on side panel canvas
                    image_id = self.side_panel_canvas.create_image(0, y_offset,anchor = 'nw', image=self.thumb_images[i])
                    text_id = self.side_panel_canvas.create_text( self.thumb_images[i].width() //2, y_offset + self.thumb_images[i].height() + 5, anchor='nw', text=self.page_number_text[i])
                
                # Store the image and text IDs
                    self.thumbnail_items.append((image_id, text_id))
                    print(self.system_cache)

        # Update y offset for next thumbnail
                    y_offset += self.thumb_image.height() + 20  # Add some padding between thumbnails
             # Save the thumbnail cache
                self.save_thumbnail_cache()
                self.load_thumbnail_cache()

    # Update scroll region of side panel canvas
            self.side_panel_canvas.config(scrollregion=self.side_panel_canvas.bbox("all"))
        
        except Exception as e:
            print(f"Error in show_side_panel: {e}")
            
    def cleanup_temp_dir(self):
        # Clean up temporary directory
            shutil.rmtree(self.temp_dir)
            print("Directory cleaned up")
            

    def clear_temp_directory(self):
        """Clears all files and directories from the specified temporary directory."""
        try:
        # List all files and directories in the specified directory
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                try:
                # Check if it is a file or directory and remove accordingly
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove the file or symbolic link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove the directory and its contents
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            print(f"All files and directories in '{self.temp_dir}' have been cleared.")
        except Exception as e:
            print(f"An error occurred while clearing the directory: {e}")



