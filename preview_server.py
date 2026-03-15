from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import webbrowser

os.chdir(r"c:\Users\user\Desktop\Reyna Moda")

class MyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost", 9000), MyHandler)
    print("✓ Servidor en http://localhost:9000")
    print("✓ Abriendo navegador...")
    webbrowser.open("http://localhost:9000/reyna_moda_completa%20(1).html")
    server.serve_forever()
