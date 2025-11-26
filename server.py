import os
import json
import smtplib
from email.message import EmailMessage
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

PORT = int(os.environ.get("PORT", "8000"))
DOC_ROOT = os.path.dirname(os.path.abspath(__file__))

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.office365.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", os.environ.get("OUTLOOK_USER", ""))
SMTP_PASS = os.environ.get("SMTP_PASS", os.environ.get("OUTLOOK_PASS", ""))
TO_EMAIL = os.environ.get("TO_EMAIL", "tour-dacap@outlook.com")

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Simple proxy for images to avoid cross-origin blocking in preview
        if self.path.startswith('/proxy-image'):
            qs = parse_qs(urlparse(self.path).query)
            src = qs.get('src', [''])[0]
            if not src:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing src parameter')
                return
            # Restrict to Unsplash image host
            parsed = urlparse(src)
            if parsed.netloc not in ('images.unsplash.com', 'source.unsplash.com'):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Unsupported host')
                return
            try:
                with urlopen(src, timeout=10) as resp:
                    content_type = resp.headers.get('Content-Type', 'image/jpeg')
                    data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Cache-Control', 'public, max-age=86400')
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(f'Proxy fetch failed: {e}'.encode('utf-8'))
            return
        # Default file serving
        return super().do_GET()
    def do_POST(self):
        if self.path == '/submit-enquiry':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode('utf-8'))
            except Exception:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid JSON')
                return

            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            interest = data.get('interest', '').strip()
            message = data.get('message', '').strip()

            if not name or not email or not message:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing required fields')
                return

            # Forward to Web3Forms
            try:
                import urllib.parse
                import urllib.request
                form_fields = {
                    'access_key': '3de52d64-cd13-46cc-ac98-d4e40ebb7c02',
                    'email': TO_EMAIL,
                    'name': name,
                    'email_from': email,
                    'phone': phone,
                    'interest': interest,
                    'message': message
                }
                data_encoded = urllib.parse.urlencode(form_fields).encode('utf-8')
                req = urllib.request.Request(
                    'https://api.web3forms.com/submit',
                    data=data_encoded,
                    headers={
                        'Accept': 'application/json',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    status = resp.getcode()
                if 200 <= status < 300:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'OK')
                else:
                    raise RuntimeError(f'Web3Forms response {status}')
            except Exception as e:
                # Fallback: write enquiry to local file
                try:
                    storage_dir = os.path.join(DOC_ROOT, 'data')
                    os.makedirs(storage_dir, exist_ok=True)
                    storage_path = os.path.join(storage_dir, 'enquiries.jsonl')
                    record = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'interest': interest,
                        'message': message,
                        'error': str(e)
                    }
                    with open(storage_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(record) + "\n")
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Stored locally; we will contact you soon.')
                except Exception as write_err:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f'Unable to send at the moment: {write_err}'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def translate_path(self, path):
        # Serve files from project root
        new_path = super().translate_path(path)
        return new_path

if __name__ == '__main__':
    os.chdir(DOC_ROOT)
    with ThreadingHTTPServer(('', PORT), Handler) as httpd:
        print(f"Serving Tour Da Cape on http://localhost:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down...")
