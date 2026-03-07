#!/usr/bin/env python3
"""
PD Newsletter Subscriber Manager
================================
Collects, stores, and manages newsletter subscribers.

Usage:
    python subscriber_manager.py add email@example.com "John Doe"
    python subscriber_manager.py list
    python subscriber_manager.py export subscribers.csv
    python subscriber_manager.py stats
    python subscriber_manager.py server  # Start webhook server
"""

import json
import csv
import sqlite3
import argparse
import os
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Paths
DATA_DIR = Path(__file__).parent / ".." / "data"
DB_PATH = DATA_DIR / "subscribers.db"
CSV_PATH = DATA_DIR / "subscribers.csv"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            source TEXT DEFAULT 'unknown',
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            last_email_sent TIMESTAMP,
            metadata TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_subscriber(email, name=None, source="manual"):
    """Add a new subscriber."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO subscribers (email, name, source, subscribed_at, is_active)
            VALUES (?, ?, ?, ?, 1)
        ''', (email.lower().strip(), name, source, datetime.now().isoformat()))
        conn.commit()
        print(f"✅ Added: {email}")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

def list_subscribers(active_only=True):
    """List all subscribers."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if active_only:
        cursor.execute('SELECT email, name, source, subscribed_at FROM subscribers WHERE is_active = 1 ORDER BY subscribed_at DESC')
    else:
        cursor.execute('SELECT email, name, source, subscribed_at, is_active FROM subscribers ORDER BY subscribed_at DESC')
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("No subscribers found.")
        return
    
    print(f"\n{'Email':<30} {'Name':<20} {'Source':<15} {'Date':<20}")
    print("-" * 90)
    for row in rows:
        email, name, source, date = row[0], row[1] or '-', row[2], row[3][:16]
        print(f"{email:<30} {name:<20} {source:<15} {date:<20}")
    
    print(f"\nTotal: {len(rows)} subscribers")

def export_to_csv(output_path=None):
    """Export subscribers to CSV."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT email, name, source, subscribed_at FROM subscribers WHERE is_active = 1')
    rows = cursor.fetchall()
    conn.close()
    
    output_path = output_path or CSV_PATH
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Email', 'Name', 'Source', 'Subscribed At'])
        writer.writerows(rows)
    
    print(f"✅ Exported {len(rows)} subscribers to {output_path}")

def show_stats():
    """Show subscriber statistics."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total counts
    cursor.execute('SELECT COUNT(*) FROM subscribers')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM subscribers WHERE is_active = 1')
    active = cursor.fetchone()[0]
    
    # By source
    cursor.execute('SELECT source, COUNT(*) FROM subscribers GROUP BY source')
    sources = cursor.fetchall()
    
    # Today's signups
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM subscribers WHERE date(subscribed_at) = ?", (today,))
    today_count = cursor.fetchone()[0]
    
    # This week
    cursor.execute("""
        SELECT COUNT(*) FROM subscribers 
        WHERE date(subscribed_at) >= date('now', '-7 days')
    """)
    week_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n📊 Newsletter Stats")
    print("=" * 40)
    print(f"Total Subscribers: {total}")
    print(f"Active: {active}")
    print(f"Unsubscribed: {total - active}")
    print(f"New Today: {today_count}")
    print(f"New This Week: {week_count}")
    
    if sources:
        print("\nBy Source:")
        for source, count in sources:
            print(f"  - {source}: {count}")

class WebhookHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for webhook submissions."""
    
    def do_POST(self):
        if self.path == '/subscribe':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                email = data.get('email', '').strip().lower()
                name = data.get('name', '').strip()
                source = data.get('source', 'webhook')
                
                if email and '@' in email:
                    add_subscriber(email, name, source)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True}).encode())
                else:
                    self.send_response(400)
                    self.end_headers()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_server(port=8000):
    """Start webhook server."""
    init_db()
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    print(f"🚀 Webhook server running on http://localhost:{port}")
    print(f"   POST /subscribe with JSON: {{'email': 'test@example.com', 'name': 'John'}}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    parser = argparse.ArgumentParser(description='Newsletter Subscriber Manager')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a subscriber')
    add_parser.add_argument('email', help='Email address')
    add_parser.add_argument('name', nargs='?', help='Subscriber name')
    add_parser.add_argument('--source', default='manual', help='Source of signup')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List subscribers')
    list_parser.add_argument('--all', action='store_true', help='Include inactive')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export to CSV')
    export_parser.add_argument('output', nargs='?', help='Output file path')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Start webhook server')
    server_parser.add_argument('--port', type=int, default=8000, help='Port number')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_subscriber(args.email, args.name, args.source)
    elif args.command == 'list':
        list_subscribers(active_only=not args.all)
    elif args.command == 'export':
        export_to_csv(args.output)
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'server':
        start_server(args.port)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
