#!/usr/bin/env python
# coding: utf-8
import http.server
import socketserver
import io
import json
from identify import identify
from model import prepare_model


PORT = 8100


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        r, info = self.deal_post_data()
        print(r, info, "by: ", self.client_address)
        f = io.BytesIO()
        if r:
            f.write(b"Success\n")
            f.write(bytes(info, 'utf-8'))

        else:
            f.write(b"Failed\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def deal_post_data(self):

        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)

        data = json.loads(self.data_string)
        with open("test_request.json", "w") as outfile:
            json.dump(data, outfile)

        return True, identify()


def main():
    prepare_model()
    Handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port" , PORT)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
else:
    print("It's file not library and executable file!")
