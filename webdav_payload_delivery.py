# Axel '0vercl0k' Souchet - Jan 4 2022
import socketserver
import http
import http.server
import os

class SimpleWebDAVRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "0vercl0k/v1337"

    def __init__(self, request, client_address, server):
        self.dll_path = server.dll_path
        self.dll_name = os.path.basename(self.dll_path)
        self.dll_size = os.path.getsize(self.dll_path)
        super().__init__(request, client_address, server)

    def send_404(self):
        self.send_error(http.HTTPStatus.NOT_FOUND, "File not found")
        return

    def do_PROPFIND(self):
        if not self.path.endswith(".dll"):
            return self.send_404()
        r = bytes(
            f"""<?xml version="1.0" ?>
<D:multistatus xmlns:D="DAV:">
  <D:response>
    <D:propstat>
      <D:prop>
        <D:name>{self.path[1:]}</D:name>
        <D:getcontenttype>application/octet-stream</D:getcontenttype>
        <D:getcontentlength>{self.dll_size}</D:getcontentlength>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
  </D:response>
</D:multistatus>""",
            "utf8",
        )
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "text/xml")
        self.send_header("Content-length", str(len(r)))
        self.end_headers()
        self.wfile.write(r)

    def do_OPTIONS(self):
        self.send_response(http.HTTPStatus.OK)
        self.send_header(
            "Allow",
            "OPTIONS, GET, HEAD, POST, DELETE, TRACE, PROPFIND, PROPPATCH, COPY, MOVE, PUT, LOCK, UNLOCK",
        )
        self.send_header("DAV", "1, 2")
        self.send_header("MS-Author-Via", "DAV")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if not self.path.endswith(".dll"):
            return self.send_404()
        content = open(self.dll_path, "rb").read()
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


class SimpleWebDAVServer(socketserver.TCPServer):
    def __init__(self, dll_path, listen_ip, port):
        self.dll_path = dll_path
        super().__init__((listen_ip, port), SimpleWebDAVRequestHandler)

def main():
    # Browse \\<ip>@80\x.dll
    payload = r'c:\windows\system32\ntdll.dll'
    local_ip = '0.0.0.0'
    port = 80
    print("Serving", payload, f"from {local_ip}:{port}...")
    webdav_server = SimpleWebDAVServer(payload, local_ip, port)
    webdav_server.serve_forever()

if __name__ == '__main__':
    main()
