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
from tkinter import filedialog
from pdf_viewer_init import PDFViewerInit
from pdf_viewer_load import PDFViewerLoad
from pdf_viewer_annotate import PDFViewerAnnotate
from pdf_viewer_cache import PDFViewerCache
from pdf_viewer_slides import PDFViewerSlides
from pdf_viewer_process import PDFViewerProcess
import os
import argparse



class PDFViewer(PDFViewerInit, PDFViewerLoad, PDFViewerAnnotate,PDFViewerCache,PDFViewerProcess):
    def __init__(self, root, display , default_pdf_path=None):
        super().__init__(root, display, default_pdf_path)

    def run(self):
        self.root.mainloop()

def upload_pdf_dialog():
    pdf_path = tk.filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    '''
    if pdf_path:
        app.load_pdf(pdf_path)
        app.run()
        '''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process for Displaying PDF")
    parser.add_argument("-l", "--local", help="Display number for local display", type=str, default='localhost:10.0')
    parser.add_argument("-r", "--remote", help="Display number for remote display", type=str, default=':0.0')
    parser.add_argument("-v", "--verbose", action='store_true', help='Enable verbose mode')

    args = parser.parse_args()
    if args.verbose:
        print("Verbose mode enabled")
        print(f'Local Display: {args.local}')
        print(f'Remote Display: {args.remote}')    

    os.environ['DISPLAY'] = args.local  # Replace ':0.0' with your desired display
    root = tk.Tk()
    pdf_path = tk.filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    #root.withdraw()
    # Get the path to the home directory
    home_dir = os.path.expanduser("~")

    if pdf_path:
        default_pdf_path = pdf_path
    else:
        default_pdf_path = os.path.join(home_dir, "smart_projector/pdf_docs/fork-exec-notes.pdf")  # Set the default PDF path here
    print(default_pdf_path)
    app = PDFViewer(root, args.remote, default_pdf_path)
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
