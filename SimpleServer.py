import os
import http.server as server
import socketserver
import logging
import cgi
import json
import urllib

if 'PORT' in os.environ:
    PORT = int(os.environ['PORT'])
    print('Got port ', PORT)
else:
    PORT = 8000


import openPitMining


class ServerHandler(server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/openPitMining.py':
            ctype, pdict = cgi.parse_header(self.headers.get_content_type())
            if ctype == 'application/json':
                length = int(self.headers.get('content-length'))
                data = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=True)
                for val in data:
                    jsdict = json.loads(val)
                    output = openPitMining.handleoptimize(jsdict)
                    output['solution'][1] = output['solution'][1].replace('\n', '<br>')
                    output = json.dumps(output)
                    output = bytes(output, "utf-8")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(output)
                    return
        else:
            server.SimpleHTTPRequestHandler.do_GET(self)


Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Starting simple server")
print("serving at port", PORT)
httpd.serve_forever()
