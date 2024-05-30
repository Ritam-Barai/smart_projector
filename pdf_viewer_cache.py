import pickle
import os
from tkinter import *
import base64
import io

class PDFViewerCache:
    def load_thumbnail_cache(self):
        try:
            with open(self.thumbnail_cache_file, "rb") as f:
                self.thumbnail_cache = pickle.load(f)
        except FileNotFoundError:
            self.thumbnail_cache = None
            
    def png_to_base64_string(self,file_path):
    # Read the binary data from the file
        with open(file_path, 'rb') as file:
            binary_data = file.read()
    
    # Encode the binary data to a base64 string
        base64_string = base64.b64encode(binary_data).decode('utf-8')
    
        return base64_string
    '''
    def base64_string_to_png(base64_string, output_file_path = 'self.temp_dir/ f"page_rest.png"'):
    # Decode the base64 string back to binary data
    
        binary_data = base64.b64decode(base64_string)
    
    # Write the binary data to a file
        with open(output_file_path, 'wb') as file:
            file.write(binary_data)
    '''
    def save_thumbnail_cache(self):
        try:
            thumbnail_data = []
            print(list(enumerate(zip(self.thumb_images, self.page_number_text))))
            print(self.thumb_images,self.page_number_text)
            for i, (thumb_image, page_number_texts) in enumerate(self.system_cache):
                image_id, text_id = self.thumbnail_items[i]
                print(thumb_image)
                thumb_string = self.png_to_base64_string(thumb_image)
                #print("binary",thumb_string)
                self.image_data = {
                    "x": self.side_panel_canvas.coords(image_id)[0],
                    "y": self.side_panel_canvas.coords(image_id)[1],
                    "photoimage": thumb_string,
                    "page_number_text": page_number_texts
                }
                thumbnail_data.append(self.image_data)
                #print(self.image_data['photoimage'])
            
                    
           # Save the updated cache
            with open(self.thumbnail_cache_file, "wb") as f:
                pickle.dump(thumbnail_data, f)

        except Exception as e:
            print(f"Error in save_thumbnail_cache: {e}")
                    
    def release_thumbnail_cache(self):
        try:
            # Delete the cache file
            if os.path.exists(self.thumbnail_cache_file):
                os.remove(self.thumbnail_cache_file)
                print("Cache cleared")
        except Exception as e:
            print(f"Error in release_thumbnail_cache: {e}")


