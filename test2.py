import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import paramiko

SSH_PORT = 22
SSH_USERNAME = 'proj'
SSH_PASSWORD = '1123'
REMOTE_PATH = '/home/proj/smart_projector/pdf_docs'

class SSHFileUploader:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Drag and Drop File Sharing")
        self.listbox = tk.Listbox(self.root, width=80, height=20)
        self.listbox.pack(pady=20)
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

    def drop(self, event):
        file_list = event.data.split()
        if len(file_list) != 1:
            messagebox.showerror("Error", "Please drop exactly one file.")
            return

        file_path = file_list[0]
        self.upload_file(file_path)

    def upload_file(self, file_path):
        try:
            transport = paramiko.Transport(('localhost', SSH_PORT))  # Use localhost or the server's IP
            transport.connect(username=SSH_USERNAME, password=SSH_PASSWORD)
            sftp = paramiko.SFTPClient.from_transport(transport)
            remote_file_path = os.path.join(REMOTE_PATH, os.path.basename(file_path))
            sftp.put(file_path, remote_file_path)
            sftp.close()
            transport.close()
            messagebox.showinfo("Success", f"File uploaded: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

def main():
    root = TkinterDnD.Tk()

    # Setup the SSH File Uploader
    uploader = SSHFileUploader(root)

    # Start the Tkinter main loop to allow drag-and-drop
    root.mainloop()

if __name__ == "__main__":
    main()
