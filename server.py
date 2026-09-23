"""Run with python server.py. Serves public/ only, never configuration or SQL files."""
import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit
from app_config import ROOT, SECURITY_HEADERS, load_env, public_config

PUBLIC = (ROOT / 'public').resolve()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def end_headers(self):
        for name, value in SECURITY_HEADERS.items():
            self.send_header(name, value)
        super().end_headers()

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path in ('/api/config', '/api/config/'):
            payload = json.dumps(public_config()).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

    def send_head(self):
        # Block dotfiles, traversal, directory listings, and links outside public/.
        path = unquote(urlsplit(self.path).path).replace('\\', '/')
        if any(part.startswith('.') for part in path.split('/') if part):
            self.send_error(404)
            return None
        target = (PUBLIC / path.lstrip('/')).resolve()
        if not target.is_relative_to(PUBLIC):
            self.send_error(404)
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404)
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hnos Palomino local preview')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--host', default='127.0.0.1')
    args = parser.parse_args()
    load_env()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f'Hnos Palomino: http://{args.host}:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
