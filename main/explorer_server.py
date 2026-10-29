"""Authenticated generator, paper demos and annotations for Render."""
from __future__ import annotations

import os
import json
import mimetypes
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

try:
    from . import agent_server as server
    from . import paper_assistant
except ImportError:
    import agent_server as server
    import paper_assistant

DEMO_ROOT = server.PROJECT_ROOT / 'docs'
ANNOTATION_BUSY = threading.Lock()
STATIC_TYPES = {'.html', '.css', '.js', '.json', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.woff2', '.pdf', '.mp4', '.mp3', '.csv', '.txt'}


class Handler(server.Handler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/healthz':
            self.send_json({'ok': True})
            return
        if path == '/demo' or path.startswith('/demo/'):
            if not server.require_basic_auth(self):
                return
            if path == '/demo':
                self.send_response(302); self.send_header('Location', '/demo/home.html'); self.end_headers()
                return
            target = (DEMO_ROOT / unquote(path[len('/demo/'):])).resolve()
            if not target.is_relative_to(DEMO_ROOT.resolve()):
                self.send_json({'error': 'Not found'}, status=404); return
            if target.is_dir():
                if not path.endswith('/'):
                    self.send_response(302); self.send_header('Location', path + '/'); self.end_headers(); return
                target = target / 'index.html'
            if target.suffix not in STATIC_TYPES or not target.is_file() or any(p.startswith('.') for p in target.relative_to(DEMO_ROOT).parts):
                self.send_json({'error': 'Not found'}, status=404); return
            body = target.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers(); self.wfile.write(body)
            return
        if path == '/api/paper-assistant/status':
            if server.require_basic_auth(self):
                self.send_json(paper_assistant.configuration())
            return
        if path in {'/', '/index.html'}:
            self.path = '/explorer'
        elif path not in server.EXPLORER_ASSETS and not path.startswith('/api/explorers/'):
            self.send_json({'error': 'Not found'}, status=404)
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/api/paper-assistant':
            if not server.require_basic_auth(self):
                return
            origin = self.headers.get('Origin')
            if origin and (urlparse(origin).scheme not in {'http', 'https'} or urlparse(origin).netloc != self.headers.get('Host')):
                self.send_json({'error': 'Cross-origin requests are not allowed.'}, status=403); return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 160000:
                    self.send_json({'error': 'Annotation request is too large.'}, status=413); return
                payload = json.loads(self.rfile.read(size))
                if not ANNOTATION_BUSY.acquire(blocking=False):
                    self.send_json({'error': 'Another annotation is being generated. Please retry shortly.'}, status=429); return
                try:
                    result = paper_assistant.respond(payload)
                finally:
                    ANNOTATION_BUSY.release()
                self.send_json(result)
            except (ValueError, UnicodeDecodeError) as exc:
                message = 'Invalid request JSON.' if isinstance(exc, (json.JSONDecodeError, UnicodeDecodeError)) else str(exc)
                self.send_json({'error': message}, status=400)
            except Exception as exc:
                self.send_json({'error': paper_assistant.safe_error(exc)}, status=502)
            return
        if path != '/api/explorers' and not path.startswith('/api/explorers/'):
            self.send_json({'error': 'Not found'}, status=404)
            return
        super().do_POST()

    def send_text(self, text, content_type='text/html; charset=utf-8', status=200):
        if 'id="generate-form"' in text:
            text = text.replace('http://127.0.0.1:8882/home.html', '/demo/home.html')
            if os.environ.get('PROOF_EXPLORER_EPHEMERAL', 'true').lower() == 'true':
                text = text.replace('<details id="composer"',
                    '<p class="prototype-note">Temporary hosting storage: download your explorer with '
                    '“Save explorer” to keep it. Server restarts clear saved runs. Keep this page open '
                    'while generation is running.</p><details id="composer"')
        super().send_text(text, content_type, status)


def main():
    # Refuse to expose a cost-incurring service without both login credentials.
    server.load_dotenv()
    if not server.basic_auth_enabled():
        raise RuntimeError('Set PROOF_AGENT_USERNAME and PROOF_AGENT_PASSWORD before starting the hosted generator.')
    if location := os.environ.get('PROOF_EXPLORER_DATA_DIR'):
        server.EXPLORERS.directory = Path(location)
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '10000'))
    with ThreadingHTTPServer((host, port), Handler) as app:
        print(f'Proof explorer listening on {host}:{port}', flush=True)
        try:
            app.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
