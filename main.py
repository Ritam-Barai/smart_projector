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
from tkinter import filedialog, messagebox
from pdf_viewer_init import PDFViewerInit
from pdf_viewer_load import PDFViewerLoad
from pdf_viewer_annotate import PDFViewerAnnotate
from pdf_viewer_cache import PDFViewerCache
from pdf_viewer_slides import PDFViewerSlides
from pdf_viewer_process import PDFViewerProcess
from pdf_viewer_fileupload import SSHFileUploader
import os
import argparse
import paramiko
import subprocess
from tkinterdnd2 import TkinterDnD, DND_FILES



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

home_dir = os.path.expanduser("~")
script_path =f"{home_dir}/smart_projector/server_proj/projview/kill_server.sh" 
def file_upload():
    # Specify the locked directory
    locked_directory = f"{home_dir}/smart_projector/server_proj/projview/media/pdfs"  # Change this to your target directory
    #print(f"Locked directory: {locked_directory}")
    if not os.path.exists(locked_directory):
        print('No Files uploaded this session')
        #subprocess.Popen(['bash', script_path], preexec_fn=os.setsid)
        messagebox.showerror("Directory does not exist:", "No Files uploaded this session. Please upload a file")
        exit(f"Directory does not exist: {locked_directory}")
    else:
        print(f"Locked directory: {locked_directory}")
        # Open the file dialog in the specified directory
        filename = filedialog.askopenfilename(
            initialdir=locked_directory,
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )

    # Ensure the selected file is within the locked directory
    if filename:
        # Get the absolute path of the locked directory and the selected file
        locked_directory_abs = os.path.abspath(locked_directory)
        selected_file_abs = os.path.abspath(filename)

        # Check if the selected file starts with the locked directory path
        if os.path.commonpath([locked_directory_abs]) == os.path.commonpath([locked_directory_abs, selected_file_abs]):
            messagebox.showinfo("Selected File", f"File selected: {filename}")
            return selected_file_abs
        else:
            messagebox.showerror("Invalid Selection", "You can only select files within the specified directory.")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process for Displaying PDF")
    parser.add_argument("-l", "--local", help="Display number for local display", type=str, default='localhost:10.0')
    parser.add_argument("-r", "--remote", help="Display number for remote display", type=str, default=':0.0')
    parser.add_argument("-i", "--ipaddress", help="IP Address for remote display", type=str, default='192.168.0.103')
    parser.add_argument("-v", "--verbose", action='store_true', help='Enable verbose mode')

    args = parser.parse_args()
    if args.verbose:
        print("Verbose mode enabled")
        print(f'Local Display {args.local}')
        print(f'Remote Display {args.remote}')
        print(f'IP Address: {args.ipaddress}')    

    #SSH_HOST = '192.168.0.103'
    SSH_PORT = 22
    SSH_USERNAME = 'proj'
    SSH_PASSWORD = '1123'
    #REMOTE_PATH = '/home/proj/smart_projector/pdf_docs'
    default_pdf_path = None

    os.environ['DISPLAY'] = args.local  # Replace ':0.0' with your desired display
    
    root = tk.Tk()
    #root.withdraw()

    # After the window closes, check for the dropped PDF file or open file dialog
    #if default_pdf_path is None:
    #pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    
    '''
    #app = SSHFileUploader(root, args.ipaddress, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, REMOTE_PATH)
    pdf_path = tk.filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    #root.withdraw()
    # Get the path to the home directory
    if pdf_path:
        default_pdf_path = pdf_path
    else:
        # Get the path to the home directory
        home_dir = os.path.expanduser("~")
        default_pdf_path = os.path.join(home_dir, "smart_projector/pdf_docs/fork-exec-notes.pdf")  # Set the default PDF path here

    print(default_pdf_path)
    '''
    default_pdf_path = file_upload()
    if default_pdf_path is None:
        #subprocess.Popen(['bash', script_path], preexec_fn=os.setsid)
        #messagebox.showerror("Directory does not exist:", "No Files uploaded this session. Please upload a file")
        exit("Wrong or no file uploaded")
    
    
    app = PDFViewer(root, args.remote, default_pdf_path)
    app.run()
    subprocess.Popen(['bash', script_path], preexec_fn=os.setsid)
    print('Exiting')
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
