import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import cgi

UPLOAD_DIRECTORY = '/home/proj/smart_projector/pdf_docs'

class SimpleUploadHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            content_type, pdict = cgi.parse_header(self.headers['content-type'])
            if content_type == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                for field in fields:
                    file_data = fields[field][0]
                    file_name = os.path.basename(field)
                    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"File uploaded successfully")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid request")
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Upload File</title>
            </head>
            <body>
                <h2>Drag and Drop File Upload</h2>
                <form method="post" enctype="multipart/form-data" action="/upload">
                    <input type="file" name="file" id="file">
                    <input type="submit" value="Upload">
                </form>
                <script>
                    const form = document.querySelector('form');
                    form.addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const fileInput = document.getElementById('file');
                        const formData = new FormData();
                        formData.append('file', fileInput.files[0]);
                        const response = await fetch('/upload', {
                            method: 'POST',
                            body: formData
                        });
                        const text = await response.text();
                        alert(text);
                    });
                </script>
            </body>
            </html>
            '''
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleUploadHTTPRequestHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()
