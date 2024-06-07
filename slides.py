import sys
import tkinter as tk
from pdf_viewer_slides import PDFViewerSlides  
import select
import selectors
import threading
import os
import argparse

class PDFSlideShow(PDFViewerSlides):
    def __init__(self, root, default_pdf_path=None):
        super().__init__(root, default_pdf_path)
        self.selector = selectors.DefaultSelector()
        self.selector.register(sys.stdin, selectors.EVENT_READ, self.read_input)

    def run(self):
        self.root.mainloop()

def read_stdin(viewer):
    while True:
        events = viewer.selector.select(timeout=1)
        for key, _ in events:
            callback = key.data
            callback()
    '''
    def read_input(self):
        ready = sys.stdin in select.select([sys.stdin], [], [])[0]
        #print(ready)
        #print("Ready",ready)
        line = sys.stdin.readline().strip()
        if line:
            self.handle_flag(line,ready)
    '''
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Subprocess for PDF Slide Show.")
    parser.add_argument("-d", "--display", help="Display number for display", type=str, required=True)
    #parser.add_argument("-v", "--verbose", action='store_true', help='Enable verbose mode')

    args = parser.parse_args()
    '''
    if args.verbose:
        print("Verbose mode enabled")
    '''
    print(f'Display Number {args.display}')
    

    os.environ['DISPLAY'] = args.display  # Replace ':0.0' with your desired display
    root = tk.Tk()
    viewer = PDFSlideShow(root)

    # Start a thread for reading stdin
    stdin_thread = threading.Thread(target=read_stdin, args=(viewer,))
    stdin_thread.daemon = True
    stdin_thread.start()

    #root.after(0, viewer.load_slide)

    viewer.run()
    
    
    '''
    for line in sys.stdin:
        slide_flag = line.strip()
        print(f"Slide Flag: {slide_flag}")
        sys.stdin.flush()
        #if slide_flag == 'START':
            #viewer.run()
        viewer.handle_flag(slide_flag,ready)
    #viewer.run()
    '''