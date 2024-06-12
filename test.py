import os
import paramiko
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

class SSHFileUploader:
    def __init__(self, root, ssh_host, ssh_port, ssh_username, ssh_password, remote_path):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.remote_path = remote_path

        self.root = root
        self.root.title('Drag and Drop File Sharing via SSH')

        self.label = tk.Label(root, text="Drag and Drop Files Here", width=40, height=10, bg='lightgray')
        self.label.pack(padx=10, pady=10)

        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            self.upload_file(file_path)

    def upload_file(self, file_path):
        try:
            transport = paramiko.Transport((self.ssh_host, self.ssh_port))
            transport.connect(username=self.ssh_username, password=self.ssh_password)
            
            sftp = paramiko.SFTPClient.from_transport(transport)
            remote_file_path = os.path.join(self.remote_path, os.path.basename(file_path))
            sftp.put(file_path, remote_file_path)
            
            sftp.close()
            transport.close()
            print(f"Successfully uploaded {file_path} to {remote_file_path}")
        except Exception as e:
            print(f"Failed to upload {file_path}: {e}")

if __name__ == "__main__":
    # SSH server details
    SSH_HOST = '192.168.0.103'
    SSH_PORT = 22
    SSH_USERNAME = 'proj'
    SSH_PASSWORD = '1123'
    REMOTE_PATH = '/home/proj/smart_projector/pdf_docs'

    root = TkinterDnD.Tk()
    app = SSHFileUploader(root, SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, REMOTE_PATH)
    root.mainloop()
