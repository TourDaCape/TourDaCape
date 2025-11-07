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
TO_EMAIL = os.environ.get("TO_EMAIL", "tourdacape1@outlook.com")

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

            # Compose email
            mail = EmailMessage()
            mail['Subject'] = 'New Tour Da Cape Enquiry'
            mail['From'] = SMTP_USER or TO_EMAIL
            mail['To'] = TO_EMAIL
            mail.set_content(
                f"New enquiry received from Tour Da Cape website.\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Interest: {interest}\n\n"
                f"Message:\n{message}\n"
            )

            # Attempt to send via Outlook SMTP; on failure, store locally and still respond 200
            try:
                if not SMTP_USER or not SMTP_PASS:
                    raise RuntimeError('SMTP credentials not configured')
                with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                    server.starttls()
                    server.login(SMTP_USER, SMTP_PASS)
                    server.send_message(mail)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
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
                    # If even local storage fails, return 500
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