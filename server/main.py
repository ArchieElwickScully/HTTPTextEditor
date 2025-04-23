from http.server import HTTPServer, BaseHTTPRequestHandler

from server.manager.request.RequestHandler import RequestHandler


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

        responseCode, response = self.rh.handlePost(body.decode("UTF-8"))
        #resp = '{' + f'"writtenResponse": "{m}", "token": "{uuid}"' + '}' # bit of a hacky way to do this but running
                                                                      # out of time -> fixed it
        self.send_response(responseCode)
        self.end_headers()

        self.wfile.write(bytes(response, encoding='utf-8'))


if __name__ == "__main__":
    PORT = 8000

    server = HTTPServer(("", PORT), HTTP)

    print("Server started on port", PORT)

    server.serve_forever()
    server.server_close()

