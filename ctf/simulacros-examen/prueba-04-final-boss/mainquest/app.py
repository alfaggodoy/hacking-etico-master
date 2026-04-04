import http.server
import socketserver
import urllib.parse
import os

PORT = 8000

class VulnerableHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed_path.query)
        
        if 'load' in qs:
            file_path = qs['load'][0]
            try:
                # VULNERABILIDAD: LFI directo
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"No existe el fichero.")
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Portal Secundario (Python)</h1><p>Visor de archivos desfasado. Ej: ?load=archivo.txt</p>")

with socketserver.TCPServer(("", PORT), VulnerableHandler) as httpd:
    print("Servidor web Python escuchando en el puerto", PORT)
    httpd.serve_forever()
