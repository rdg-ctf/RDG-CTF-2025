import http.server
import socketserver

PORT = 13337
DIRECTORY = "www"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def list_directory(self, *args, **kwargs):
        return


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.allow_reuse_address = True
    
    print("serving at port", PORT)
    httpd.serve_forever()
