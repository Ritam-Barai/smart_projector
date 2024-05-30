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

    def save_thumbnail_cache(self):
        try:
            thumbnail_data = []
            print(list(enumerate(zip(self.thumb_images, self.page_number_text))))
            print(self.thumb_images,self.page_number_text)
            for i, (thumb_image, page_number_texts) in enumerate(zip(self.thumb_images, self.page_number_text)):
                image_id, text_id = self.thumbnail_items[i]
                print(thumb_image,thumb_image.width())
                with io.BytesIO() as f:
                    thumb_image.write(f, format='PNG') 
                    thumb_img = base64.b64encode(f.getvalue()).decode('utf-8')
                    print("binary",f.getvalue())
                self.image_data = {
                    "x": self.side_panel_canvas.coords(image_id)[0],
                    "y": self.side_panel_canvas.coords(image_id)[1],
                    "photoimage": thumb_img,
                    "page_number_text": page_number_texts
                }
                thumbnail_data.append(self.image_data)
                print(self.image_data['photoimage'])
            
                    
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


