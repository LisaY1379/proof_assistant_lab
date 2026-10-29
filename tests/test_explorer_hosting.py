"""Exercise the hosted HTTP boundary without credentials or model requests."""
import base64
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


class HostedExplorerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        files = ['main/'+f for f in ['agent_server.py', 'explorer_server.py',
                 'explorer_service.py', 'explorer_pipeline.py', 'explorer_protocol.py', 'paper_assistant.py']]
        files += ['main/explorer/'+f for f in ['index.html', 'app.js', 'styles.css', 'example.json']]
        files += ['tools/proof_explorer/'+f for f in ['styles.css', 'proof-reader.css',
                  'protocol-reference.html', 'protocol.html']]
        files += ['tools/proof_explorer/papers/high-contrast/'+f for f in ['index.html','paper-data.json']]
        files += ['docs/home.html']
        files += ['docs/papers/high-contrast/'+f for f in ['index.html','dictionary.js','dictionary-data.js','dictionary.css','annotation-format.js','assistant.js','assistant.css']]
        for name in files:
            dest = cls.root/name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/name, dest)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        cls.url = f'http://127.0.0.1:{port}'
        cls.env = {**os.environ, 'HOST': '127.0.0.1', 'PORT': str(port),
                   'PROOF_AGENT_USERNAME': 'test', 'PROOF_AGENT_PASSWORD': 'test-only-password',
                   'PROOF_EXPLORER_DATA_DIR': str(cls.root/'runs'), 'OPENAI_API_KEY': ''}
        cls.proc = subprocess.Popen([sys.executable, 'main/explorer_server.py'], cwd=cls.root,
                                    env=cls.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            try:
                urllib.request.urlopen(cls.url+'/healthz', timeout=1).close()
                return
            except urllib.error.URLError:
                if cls.proc.poll() is not None:
                    raise RuntimeError('Hosted server failed to start')
                time.sleep(.1)
        cls.proc.terminate()
        raise RuntimeError('Hosted server did not become healthy')

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait(timeout=5)
        cls.temp.cleanup()

    def request(self, path, *, authenticated=False, payload=None):
        headers = {}
        if authenticated:
            headers['Authorization'] = 'Basic '+base64.b64encode(b'test:test-only-password').decode()
        if payload is not None:
            headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(self.url+path, headers=headers,
                                     data=None if payload is None else json.dumps(payload).encode())
        try:
            response = urllib.request.urlopen(req, timeout=5)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            return response.status, response.read().decode()

    def test_public_health_does_not_expose_generator_or_jobs(self):
        self.assertEqual(self.request('/healthz'), (200, '{\n  "ok": true\n}'))
        for path in ['/', '/explorer/app.js', '/api/explorers/'+'a'*32]:
            self.assertEqual(self.request(path)[0], 401)
        self.assertEqual(self.request('/api/explorers', payload={})[0], 401)
        self.assertEqual(self.request('/.env')[0], 404)

    def test_generator_home_and_static_dependencies(self):
        status, page = self.request('/', authenticated=True)
        self.assertEqual(status, 200)
        self.assertIn('id="generate-form"', page)
        self.assertIn('Temporary hosting storage', page)
        self.assertIn('Explore the demo', page)
        self.assertIn('/demo/home.html', page)
        self.assertNotIn('http://127.0.0.1:8882', page)
        for path in ['/explorer/app.js', '/explorer/styles.css', '/explorer/base.css', '/explorer/reader.css']:
            self.assertEqual(self.request(path, authenticated=True)[0], 200)
        self.assertEqual(self.request('/api/chat', authenticated=True, payload={})[0], 404)

    def test_demo_and_annotations_require_authentication(self):
        for path in ['/demo/home.html','/demo/papers/high-contrast/','/api/paper-assistant/status']:
            self.assertEqual(self.request(path)[0],401)
            self.assertEqual(self.request(path,authenticated=True)[0],200)
        self.assertEqual(self.request('/api/paper-assistant',payload={})[0],401)
        self.assertEqual(self.request('/api/paper-assistant',authenticated=True,payload={})[0],400)
        for path in ['/demo/../main/agent_server.py','/demo/%2e%2e/.env','/demo/.env']:
            self.assertEqual(self.request(path,authenticated=True)[0],404)
        for asset in ['dictionary.js','dictionary-data.js','dictionary.css','annotation-format.js','assistant.js']:
            self.assertEqual(self.request('/demo/papers/high-contrast/'+asset,authenticated=True)[0],200)
        req=urllib.request.Request(self.url+'/api/paper-assistant',data=b'{}',headers={
            'Origin':'https://elsewhere.example',
            'Authorization':'Basic '+base64.b64encode(b'test:test-only-password').decode()})
        with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(req)
        self.assertEqual(error.exception.code,403)

    def test_import_and_read_saved_explorer_without_api_key(self):
        document = json.loads((self.root/'main/explorer/example.json').read_text())
        status, body = self.request('/api/explorers/import', authenticated=True, payload=document)
        self.assertEqual(status, 200)
        job = json.loads(body)
        self.assertTrue((self.root/'runs'/f"{job['id']}.json").is_file())
        status, body = self.request('/api/explorers/'+job['id'], authenticated=True)
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(body)['document']['closure'])
        status, body = self.request('/api/explorers', authenticated=True, payload={'proof': 'Test'})
        self.assertEqual(status, 400)
        self.assertIn('Configure OPENAI_API_KEY', body)

    def test_hosted_startup_requires_login_configuration(self):
        result = subprocess.run([sys.executable, 'main/explorer_server.py'], cwd=self.root,
                                env={**self.env, 'PROOF_AGENT_PASSWORD': ''}, capture_output=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'Set PROOF_AGENT_USERNAME and PROOF_AGENT_PASSWORD', result.stderr)


if __name__ == '__main__':
    unittest.main()
