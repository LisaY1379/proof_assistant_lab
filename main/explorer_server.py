"""Password-protected, generator-only entry point for Render."""
from __future__ import annotations

import os
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

try:
    from . import agent_server as server
except ImportError:
    import agent_server as server


class Handler(server.Handler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/healthz':
            self.send_json({'ok': True})
            return
        if path in {'/', '/index.html'}:
            self.path = '/explorer'
        elif path not in server.EXPLORER_ASSETS and not path.startswith('/api/explorers/'):
            self.send_json({'error': 'Not found'}, status=404)
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path != '/api/explorers' and not path.startswith('/api/explorers/'):
            self.send_json({'error': 'Not found'}, status=404)
            return
        super().do_POST()

    def send_text(self, text, content_type='text/html; charset=utf-8', status=200):
        if 'id="generate-form"' in text:
            text = text.replace('<a href="/">AI conversation</a>',
                                '<a href="https://lisay1379.github.io/proof_assistant_lab/">Five-theorem explorers</a>')
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
