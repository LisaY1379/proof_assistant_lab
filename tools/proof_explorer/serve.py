#!/usr/bin/env python3
"""Serve the local explorer and its contextual AI assistant on loopback only."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import sys
import threading

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from main import paper_assistant
BUSY = threading.Lock()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def trusted(self):
        host = self.headers.get('Host')
        return (host in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}')
                and self.headers.get('Origin') in (None, 'http://' + host))

    def send_json(self, value, status=200):
        data = json.dumps(value).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def do_GET(self):
        if not self.trusted():
            return self.send_json({'error': 'Open this explorer at its localhost address.'}, 403)
        path = urlparse(self.path).path
        if path == '/api/paper-assistant/status':
            return self.send_json(paper_assistant.configuration())
        target = Path(self.translate_path(path)).resolve()
        if not target.is_relative_to(HERE) or target.suffix not in ('.html', '.js', '.css', '.json', '.svg', '.png', '.jpg', '.jpeg', '.woff2', '.pdf', ''):
            return self.send_error(404)
        if target.is_dir() and not (target / 'index.html').is_file():
            return self.send_error(404)
        super().do_GET()

    def do_POST(self):
        if not self.trusted():
            return self.send_json({'error': 'Cross-origin requests are not allowed.'}, 403)
        if urlparse(self.path).path != '/api/paper-assistant':
            return self.send_error(404)
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 160000:
                return self.send_json({'error': 'Discussion request is too large.'}, 413)
            payload = json.loads(self.rfile.read(size))
            if not BUSY.acquire(blocking=False):
                return self.send_json({'error': 'Another answer is being generated. Please retry shortly.'}, 409)
            try:
                result = paper_assistant.respond(payload)
            finally:
                BUSY.release()
            return self.send_json(result)
        except ValueError as exc:
            return self.send_json({'error': str(exc) if not isinstance(exc, json.JSONDecodeError) else 'Invalid request JSON.'}, 400)
        except Exception as exc:
            return self.send_json({'error': paper_assistant.safe_error(exc)}, 502)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8882)
    args = parser.parse_args()
    with ThreadingHTTPServer(('127.0.0.1', args.port), Handler) as server:
        print(f'Paper explorer: http://127.0.0.1:{args.port}/papers/high-contrast/', flush=True)
        server.serve_forever()
