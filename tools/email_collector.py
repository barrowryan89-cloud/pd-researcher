#!/usr/bin/env python3
"""
Email Collection Endpoint
=========================
Simple Formspree alternative for collecting newsletter signups.
Drop this on a server with Python and collect emails to a JSON file.

Setup:
    1. Upload to your server
    2. Run: python email_collector.py
    3. Update newsletter_signup.html with your server URL
    4. Emails collect to data/emails.json
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("data/emails.json")
DATA_FILE.parent.mkdir(exist_ok=True)

class EmailCollectorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/collect':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length:
                post_data = self.rfile.read(content_length).decode('utf-8')
                params = {}
                for param in post_data.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params[key] = urllib.parse.unquote_plus(value)
                
                self.save_email(params.get('email'), params.get('name'))
            
            # Redirect to thank you page
            self.send_response(302)
            self.send_header('Location', '/thanks.html')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/stats':
            count = self.get_count()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"subscribers": count}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def save_email(self, email, name=None):
        if not email or '@' not in email:
            return
        
        emails = []
        if DATA_FILE.exists():
            with open(DATA_FILE) as f:
                emails = json.load(f)
        
        # Check for duplicates
        if not any(e['email'] == email.lower() for e in emails):
            emails.append({
                'email': email.lower(),
                'name': name,
                'date': datetime.now().isoformat(),
                'ip': self.client_address[0]
            })
            
            with open(DATA_FILE, 'w') as f:
                json.dump(emails, f, indent=2)
            
            print(f"📧 New subscriber: {email}")
    
    def get_count(self):
        if DATA_FILE.exists():
            with open(DATA_FILE) as f:
                return len(json.load(f))
        return 0
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    import urllib.parse
    
    PORT = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', PORT), EmailCollectorHandler)
    print(f"📬 Email collector running on port {PORT}")
    print(f"   POST /collect to add emails")
    print(f"   GET /stats for subscriber count")
    server.serve_forever()
