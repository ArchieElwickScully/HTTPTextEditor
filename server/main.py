from http.server import HTTPServer, BaseHTTPRequestHandler

from server.manager.RequestHandler import RequestHandler


class HTTP(BaseHTTPRequestHandler):
    rh = RequestHandler()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        #self.wfile.write(bytes(""))

    def do_POST(self):
        length = int(self.headers['Content-length'])
        body = self.rfile.read(length)

        response, m, uuid = self.rh.handlePost(body.decode("UTF-8"))

        self.send_response(response)
        self.end_headers()

        self.wfile.write(bytes(m, encoding='utf-8'))


def main():
    PORT = 8000

    server = HTTPServer(("", PORT), HTTP)

    print("Server started on port", PORT)

    server.serve_forever()
    server.server_close()


if __name__ == "__main__":
    main()
