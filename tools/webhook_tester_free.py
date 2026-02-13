#!/usr/bin/env python3
"""
Webhook Tester & Receiver — Tool #52
Local webhook endpoint for testing callbacks and integrations.
Part of the 50+ Free CLI Tools collection.
https://github.com/barrowryan89-cloud/pd-researcher
"""

import argparse
import json
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Store received webhooks in memory
webhook_history = []

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass
    
    def do_GET(self):
        self._handle_request("GET")
    
    def do_POST(self):
        self._handle_request("POST")
    
    def do_PUT(self):
        self._handle_request("PUT")
    
    def do_DELETE(self):
        self._handle_request("DELETE")
    
    def do_PATCH(self):
        self._handle_request("PATCH")
    
    def _handle_request(self, method):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Flatten single-value query params
        query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        
        # Read body
        content_length = self.headers.get('Content-Length')
        body = ""
        if content_length:
            try:
                body = self.rfile.read(int(content_length)).decode('utf-8')
            except:
                body = "<binary or unreadable content>"
        
        # Parse JSON body if applicable
        parsed_body = None
        content_type = self.headers.get('Content-Type', '')
        if 'application/json' in content_type and body:
            try:
                parsed_body = json.loads(body)
            except:
                parsed_body = None
        
        # Build webhook record
        webhook = {
            "id": len(webhook_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "path": self.path,
            "headers": dict(self.headers),
            "query_params": query_params,
            "body": body if not parsed_body else None,
            "json_body": parsed_body,
        }
        
        webhook_history.append(webhook)
        
        # Print to console
        self._print_webhook(webhook)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "received",
            "webhook_id": webhook["id"],
            "message": "Webhook captured successfully"
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def _print_webhook(self, webhook):
        print(f"\n{'='*60}")
        print(f"🪝 WEBHOOK #{webhook['id']} RECEIVED")
        print(f"{'='*60}")
        print(f"📅 {webhook['timestamp']}")
        print(f"🔹 Method: {webhook['method']}")
        print(f"🔹 Path: {webhook['path']}")
        
        if webhook['query_params']:
            print(f"\n📋 Query Parameters:")
            for k, v in webhook['query_params'].items():
                print(f"   {k}: {v}")
        
        print(f"\n📨 Headers:")
        for k, v in webhook['headers'].items():
            print(f"   {k}: {v}")
        
        if webhook['json_body']:
            print(f"\n📦 JSON Body:")
            print(json.dumps(webhook['json_body'], indent=2))
        elif webhook['body']:
            print(f"\n📄 Body:")
            print(webhook['body'][:1000])  # Truncate if very long
            if len(webhook['body']) > 1000:
                print(f"   ... ({len(webhook['body']) - 1000} more chars)")
        
        print(f"{'='*60}\n")

def run_server(port, max_history):
    server = HTTPServer(('', port), WebhookHandler)
    print(f"🚀 Webhook receiver started on http://localhost:{port}")
    print(f"📊 Max history: {max_history} webhooks")
    print(f"🛑 Press Ctrl+C to stop\n")
    print(f"Send webhooks to: http://localhost:{port}/webhook")
    print(f"Or any path: http://localhost:{port}/any/path/you/want")
    print(f"\n{'='*60}\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        print(f"📈 Total webhooks received: {len(webhook_history)}")
        sys.exit(0)

def show_history(limit=10):
    """Display webhook history"""
    if not webhook_history:
        print("No webhooks received yet.")
        return
    
    print(f"\n📜 Last {min(limit, len(webhook_history))} webhooks:")
    print("-" * 60)
    
    for wh in reversed(webhook_history[-limit:]):
        print(f"#{wh['id']} | {wh['method']} | {wh['path'][:40]} | {wh['timestamp'][:19]}")
    
    print()

def export_history(filepath):
    """Export webhook history to JSON file"""
    if not webhook_history:
        print("No webhooks to export.")
        return
    
    with open(filepath, 'w') as f:
        json.dump(webhook_history, f, indent=2)
    
    print(f"✅ Exported {len(webhook_history)} webhooks to {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Webhook Tester & Receiver — Test HTTP callbacks locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start server on port 8080
  %(prog)s -p 3000            # Start on port 3000
  %(prog)s --history          # Show received webhooks
  %(prog)s --export hooks.json # Export to JSON file

Stripe webhook example:
  stripe listen --forward-to localhost:8080/webhook
        """
    )
    
    parser.add_argument('-p', '--port', type=int, default=8080,
                       help='Port to listen on (default: 8080)')
    parser.add_argument('--max-history', type=int, default=100,
                       help='Maximum webhooks to keep in memory (default: 100)')
    parser.add_argument('--history', action='store_true',
                       help='Show webhook history and exit')
    parser.add_argument('--export', metavar='FILE',
                       help='Export webhook history to JSON file')
    parser.add_argument('--version', action='version', version='Webhook Tester 1.0.0')
    
    args = parser.parse_args()
    
    if args.history:
        show_history()
        return
    
    if args.export:
        export_history(args.export)
        return
    
    run_server(args.port, args.max_history)

if __name__ == "__main__":
    main()
