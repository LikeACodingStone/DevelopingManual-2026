"""UTF-8 JSON POST with a local server; all lengths count bytes."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from urllib.request import Request, urlopen

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/echo':
            self.send_error(404)
            return
        size = int(self.headers.get('Content-Length', '0'))
        if not 0 < size <= 4096:
            self.send_error(413)
            return
        try:
            value = json.loads(self.rfile.read(size))
        except (ValueError, UnicodeError):
            self.send_error(400)
            return
        body = json.dumps(value, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

def demo():
    with HTTPServer(('127.0.0.1', 0), Handler) as server:
        server.timeout = 5
        thread = threading.Thread(target=server.handle_request)
        thread.start()
        try:
            body = json.dumps({'text': '你好 PCM'}, ensure_ascii=False).encode('utf-8')
            request = Request(f'http://127.0.0.1:{server.server_port}/echo', data=body,
                              headers={'Content-Type': 'application/json'}, method='POST')
            with urlopen(request, timeout=5) as response:
                result = json.load(response)
            if result != {'text': '你好 PCM'}:
                raise RuntimeError('response mismatch')
        finally:
            thread.join(timeout=6)
        if thread.is_alive():
            raise RuntimeError('server did not terminate')
        print('HTTP JSON echo OK')

if __name__ == '__main__':
    demo()
