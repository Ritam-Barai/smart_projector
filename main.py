'''
import tkinter as tk
from pdf_viewer import PDFViewer

def main():
    root = tk.Tk()
    default_pdf_path = "/home/ritam/smart_projector/server_proj/projview/pdf_view/static/fork-exec-notes.pdf"  # Set the default PDF path here
    app = PDFViewer(root, default_pdf_path)
    app.run()

if __name__ == "__main__":
    main()

'''
import tkinter as tk
from pdf_viewer_init import PDFViewerInit
from pdf_viewer_load import PDFViewerLoad
from pdf_viewer_annotate import PDFViewerAnnotate
from pdf_viewer_cache import PDFViewerCache
import os

class PDFViewer(PDFViewerInit, PDFViewerLoad, PDFViewerAnnotate,PDFViewerCache):
    def __init__(self, root, default_pdf_path=None):
        super().__init__(root, default_pdf_path)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    # Get the path to the home directory
    home_dir = os.path.expanduser("~")
    os.environ['DISPLAY'] = 'localhost:10.0'  # Replace ':0.0' with your desired display
    
    default_pdf_path = os.path.join(home_dir, "smart_projector/server_proj/projview/pdf_view/static/fork-exec-notes.pdf")  # Set the default PDF path here
    print(default_pdf_path)
    app = PDFViewer(root, default_pdf_path)
    app.run()
'''
import tkinter as tk
from pdf_viewer_init import PDFViewerInit
from pdf_viewer_load import PDFViewerLoad
from pdf_viewer_annotate import PDFViewerAnnotate

class PDFViewerApp(PDFViewerInit, PDFViewerLoad, PDFViewerAnnotate):
    def __init__(self, root, default_pdf_path=None):
        self.root = root
        self.root.title("PDF Viewer")

        # Initialize PDFViewerInit and PDFViewerLoad
        self.pdf_viewer_init = super().__init__(self.root, default_pdf_path)
        self.pdf_viewer_load = PDFViewerLoad(self.root, self.pdf_viewer_init)

        # Initialize PDFViewerAnnotate
        self.pdf_viewer_annotate = PDFViewerAnnotate(self.root, self.pdf_viewer_init)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    default_pdf_path = "/path/to/default.pdf"  # Set the default PDF path here
    app = PDFViewerApp(root, default_pdf_path)
    app.pdf_viewer_load.load_pdf()  # Call load_pdf method to load the default PDF
    app.run()
'''
