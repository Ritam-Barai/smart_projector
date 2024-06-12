import os
import paramiko
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES


class SSHFileUploader:
    def __init__(self, root, ipaddress, port, username, password, remote_path):
        self.ipaddress = ipaddress
        self.port = port
        self.username = username
        self.password = password
        self.remote_path = remote_path
        self.root = root
        #self.message_box = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Drag and Drop File Sharing")
        #self.listbox = tk.Listbox(self.root, width=40, height=10)
        #elf.listbox.pack(pady=10)

        self.label = tk.Label(self.root, text="Drag and Drop Files Here", width=40, height=10, bg='lightgray')
        self.label.pack(padx=10, pady=10)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)
        self.file_selected = False

    def drop(self, event):
        file_list = event.data.split()
        if len(file_list) != 1:
            messagebox.showerror("Error", "Please drop exactly one file.")
            return
        else:
        #for file_path in file_list:
            self.upload_file(file_list[0])
            self.file_selected = True
            #self.listbox.insert(tk.END, file_path)
            self.root.quit()
        #self.root.after(2000, self.root.quit)  # Close the window after 2 seconds

    def upload_file(self, file_path):
        try:
            transport = paramiko.Transport((self.ipaddress, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            remote_file_path = os.path.join(self.remote_path, os.path.basename(file_path))
            sftp.put(file_path, remote_file_path)
            sftp.close()
            transport.close()
            messagebox.showinfo("Success", f"File uploaded: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

    def run_file_dialog_on_server(self):
        command = 'python -c "import tkinter as tk; from tkinter import filedialog; root = tk.Tk(); root.withdraw(); filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])"'
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ipaddress, port=self.port, username=self.username, password=self.password)
            stdin, stdout, stderr = ssh.exec_command(command)
            file_path = stdout.read().strip().decode()
            ssh.close()
            return file_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run file dialog on server: {e}")
            return None

        '''  
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

        '''