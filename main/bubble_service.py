"""Invite-authenticated AI requests for the Bubble desktop beta."""
import hashlib
import hmac
import json
import os
import threading
import time
from collections import deque
from contextlib import contextmanager
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pathlib import Path

ROUTES = {'/bubble/v1/chat/completions': 'chat/completions', '/bubble/v1/responses': 'responses'}
lock = threading.Lock()
recent = {}
running = set()


def authenticated(token):
    configured = os.environ.get('BUBBLE_INVITE_HASHES')
    if configured is None:
        configured = Path(__file__).with_name('bubble-invites.txt').read_text()
    digest = hashlib.sha256(token.encode()).hexdigest()
    return digest if token and any(hmac.compare_digest(digest, item) for item in configured.split()) else None


@contextmanager
def allowance(identity):
    now = time.monotonic()
    with lock:
        usage = recent.setdefault(identity, deque())
        while usage and usage[0] <= now - 86400:
            usage.popleft()
        if identity in running or len(usage) >= 60 or sum(t > now - 60 for t in usage) >= 8:
            raise OverflowError
        usage.append(now)
        running.add(identity)
    try:
        yield
    finally:
        with lock:
            running.discard(identity)


def build_payload(route, data):
    if not isinstance(data, dict):
        raise ValueError
    responses = route == 'responses'
    source = data.get('input' if responses else 'messages')
    if isinstance(source, list):
        for msg in source:
            if not isinstance(msg, dict) or set(msg) != {'role','content'} or msg['role'] not in ('system','user','assistant'):
                raise ValueError
            if isinstance(msg['content'], str):
                continue
            if not isinstance(msg['content'], list):
                raise ValueError
            for part in msg['content']:
                if not isinstance(part, dict):
                    raise ValueError
                if part.get('type') == ('input_text' if responses else 'text') and set(part)=={'text','type'} and isinstance(part['text'], str):
                    continue
                if responses:
                    image = part.get('image_url')
                    valid = set(part) <= {'type','image_url','detail'} and part.get('type') == 'input_image'
                else:
                    spec = part.get('image_url')
                    valid = part.get('type') == 'image_url' and set(part)=={'type','image_url'} and isinstance(spec,dict) and set(spec)<= {'detail','url'}
                    image = spec.get('url') if valid else None
                if not valid or not isinstance(image,str) or not image.startswith(('data:image/png;base64,','data:image/jpeg;base64,')):
                    raise ValueError
    elif not (responses and isinstance(source,str)):
        raise ValueError
    output_key = 'max_output_tokens' if responses else 'max_completion_tokens'
    limit = data.get(output_key,4000)
    if type(limit) is not int or limit < 1:
        raise ValueError
    payload = {'model': os.environ.get('BUBBLE_MODEL','gpt-4.1'), 'store':False,
               'stream':data.get('stream') is True,output_key:min(limit,10000),
               'input' if responses else 'messages':source}
    if responses:
        for key in ('instructions','text'):
            if key in data:
                payload[key]=data[key]
        if data.get('tools'):
            payload.update(tools=[{'type':'web_search'}],max_tool_calls=2,
                           tool_choice='required' if data.get('tool_choice')=='required' else 'auto',
                           include=['web_search_call.action.sources'])
    elif 'response_format' in data:
        payload['response_format']=data['response_format']
    return payload


def handle(handler,path):
    token = handler.headers.get('Authorization','')
    identity = authenticated(token[7:]) if token.startswith('Bearer ') else None
    if not identity:
        return handler.send_json({'error':'A valid Bubble invite is required.'},status=401)
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        return handler.send_json({'error':'The hosted API key is missing.'},status=503)
    if path == '/bubble/status':
        return handler.send_json({'ready':True})
    started = False
    try:
        length = int(handler.headers.get('Content-Length','0'))
        if not 0 < length <= 28_000_000:
            return handler.send_json({'error':'Request body outside supported size.'},status=413)
        with allowance(identity):
            route = ROUTES[path]
            payload = build_payload(route,json.loads(handler.rfile.read(length)))
            request = Request('https://api.openai.com/v1/'+route,data=json.dumps(payload).encode(),
                              headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
            with urlopen(request,timeout=150) as upstream:
                started = True
                handler.send_response(200)
                handler.send_header('Content-Type',upstream.headers.get('Content-Type','application/json'))
                handler.send_header('Cache-Control','no-store')
                handler.send_header('Connection','close')
                handler.end_headers()
                handler.close_connection=True
                while chunk := upstream.read1(65536):
                    handler.wfile.write(chunk)
                    handler.wfile.flush()
    except HTTPError as exc:
        status=502 if exc.code==401 else exc.code
        handler.send_json({'error':'Hosted API key rejected.' if exc.code==401 else 'AI provider returned HTTP '+str(exc.code)},status=status)
    except (BrokenPipeError,ConnectionResetError):
        return
    except (URLError,TimeoutError):
        if not started:
            handler.send_json({'error':'AI provider unavailable.'},status=502)
    except OverflowError:
        handler.send_json({'error':'Beta request limit reached or another request is running.'},status=429)
    except (ValueError,UnicodeError,RecursionError):
        handler.send_json({'error':'Unsupported Bubble request.'},status=400)
