#!/usr/bin/env python3
"""Dev server: serves frontend static files and proxies /api/ to the backend."""
import http.server
import urllib.request
import urllib.error

FRONTEND_DIR = "frontend"
BACKEND = "http://localhost:8000"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._proxy()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self._proxy()
        else:
            self.send_error(405)

    def _proxy(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else None
        req = urllib.request.Request(
            BACKEND + self.path,
            data=body,
            method=self.command,
            headers={k: v for k, v in self.headers.items()
                     if k.lower() not in ("host", "content-length")},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(e.read())

    def log_message(self, fmt, *args):
        print(fmt % args)


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with http.server.HTTPServer(("", 8080), Handler) as httpd:
        print("Dev server at http://localhost:8080")
        httpd.serve_forever()
