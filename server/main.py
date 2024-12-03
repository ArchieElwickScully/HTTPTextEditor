from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000


class HTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        #self.wfile.write(bytes(""))


server = HTTPServer(("", PORT), HTTP)

print("Server started on port", PORT)

server.serve_forever()
server.server_close()
