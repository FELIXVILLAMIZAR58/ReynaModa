from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import webbrowser
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

os.chdir(r"c:\Users\user\Desktop\Reyna Moda")

clients = []

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/subscribe':
            clients.append(self)
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            try:
                while True:
                    time.sleep(1)
            except:
                if self in clients:
                    clients.remove(self)
        else:
            return super().do_GET()
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and (event.src_path.endswith('.html') or event.src_path.endswith('.css') or event.src_path.endswith('.js')):
            print(f"✓ Cambio detectado: {os.path.basename(event.src_path)}")
            notify_clients()

def notify_clients():
    for client in clients[:]:
        try:
            client.wfile.write(b"data: reload\n\n")
        except:
            clients.remove(client)

if __name__ == "__main__":
    # Iniciar observador de cambios
    observer = Observer()
    observer.schedule(FileChangeHandler(), '.', recursive=True)
    observer.start()
    
    server = HTTPServer(("localhost", 9000), MyHandler)
    print("✓ Servidor en http://localhost:9000")
    print("✓ Abriendo navegador...")
    webbrowser.open("http://localhost:9000/index.html")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
