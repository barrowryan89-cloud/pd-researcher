#!/usr/bin/env python3
"""
Tool #31: website_monitor
Simple uptime and response time monitoring for websites.
Logs to CSV, alerts on downtime.
"""

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import ssl

# Create SSL context that doesn't verify certs (for monitoring purposes)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

CONFIG_PATH = Path.home() / ".website_monitor.json"
LOG_PATH = Path.home() / ".website_monitor_logs.csv"

def load_config():
    """Load monitored sites from config"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"sites": [], "timeout": 10}

def save_config(config):
    """Save config to file"""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def check_site(url, timeout=10):
    """Check a single site and return status info"""
    start_time = time.time()
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Monitor/1.0)'})
        with urlopen(req, timeout=timeout, context=ssl_context) as response:
            response_time = (time.time() - start_time) * 1000  # ms
            return {
                "url": url,
                "status": response.status,
                "up": 200 <= response.status < 400,
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat(),
                "error": None
            }
    except HTTPError as e:
        return {
            "url": url,
            "status": e.code,
            "up": False,
            "response_time_ms": None,
            "timestamp": datetime.now().isoformat(),
            "error": str(e.reason)
        }
    except URLError as e:
        return {
            "url": url,
            "status": None,
            "up": False,
            "response_time_ms": None,
            "timestamp": datetime.now().isoformat(),
            "error": str(e.reason)
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "up": False,
            "response_time_ms": None,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

def log_result(result):
    """Log check result to CSV"""
    file_exists = LOG_PATH.exists()
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "url", "status", "up", "response_time_ms", "error"])
        writer.writerow([
            result["timestamp"],
            result["url"],
            result["status"],
            result["up"],
            result["response_time_ms"],
            result["error"]
        ])

def add_site(url):
    """Add a site to monitor"""
    config = load_config()
    if url not in config["sites"]:
        config["sites"].append(url)
        save_config(config)
        print(f"✅ Added {url} to monitoring")
    else:
        print(f"⚠️ {url} already monitored")

def remove_site(url):
    """Remove a site from monitoring"""
    config = load_config()
    if url in config["sites"]:
        config["sites"].remove(url)
        save_config(config)
        print(f"✅ Removed {url} from monitoring")
    else:
        print(f"⚠️ {url} not in monitoring list")

def list_sites():
    """List all monitored sites"""
    config = load_config()
    if not config["sites"]:
        print("No sites configured. Use 'add' to add sites.")
        return
    
    print(f"\n📊 Monitored Sites ({len(config['sites'])}):")
    print("-" * 50)
    for site in config["sites"]:
        print(f"  • {site}")
    print()

def check_all():
    """Check all configured sites"""
    config = load_config()
    if not config["sites"]:
        print("No sites configured. Use 'add' to add sites.")
        return
    
    print(f"\n🔍 Checking {len(config['sites'])} sites...")
    print("-" * 60)
    
    any_down = False
    for url in config["sites"]:
        result = check_site(url, config.get("timeout", 10))
        log_result(result)
        
        status_icon = "🟢" if result["up"] else "🔴"
        status_text = "UP" if result["up"] else "DOWN"
        response_str = f"{result['response_time_ms']}ms" if result["response_time_ms"] else "N/A"
        
        print(f"{status_icon} {url}")
        print(f"   Status: {result['status']} ({status_text})")
        print(f"   Response: {response_str}")
        if result["error"]:
            print(f"   Error: {result['error']}")
        print()
        
        if not result["up"]:
            any_down = any_down or True
    
    if any_down:
        print("⚠️  Some sites are down!")
    else:
        print("✅ All sites operational")
    
    return any_down

def show_stats():
    """Show statistics from logs"""
    if not LOG_PATH.exists():
        print("No logs found. Run 'check' first.")
        return
    
    with open(LOG_PATH) as f:
        reader = csv.DictReader(f)
        logs = list(reader)
    
    if not logs:
        print("No log data available.")
        return
    
    print(f"\n📈 Statistics ({len(logs)} total checks):")
    print("-" * 40)
    
    # Calculate per-site stats
    sites = {}
    for log in logs:
        url = log["url"]
        if url not in sites:
            sites[url] = {"checks": 0, "up": 0, "down": 0, "response_times": []}
        sites[url]["checks"] += 1
        if log["up"] == "True":
            sites[url]["up"] += 1
        else:
            sites[url]["down"] += 1
        if log["response_time_ms"] and log["response_time_ms"] != "":
            sites[url]["response_times"].append(float(log["response_time_ms"]))
    
    for url, stats in sites.items():
        uptime_pct = (stats["up"] / stats["checks"] * 100) if stats["checks"] > 0 else 0
        avg_response = sum(stats["response_times"]) / len(stats["response_times"]) if stats["response_times"] else 0
        
        print(f"\n{url}")
        print(f"  Checks: {stats['checks']} | Up: {stats['up']} | Down: {stats['down']}")
        print(f"  Uptime: {uptime_pct:.1f}% | Avg Response: {avg_response:.0f}ms")

def clear_logs():
    """Clear all logs"""
    if LOG_PATH.exists():
        LOG_PATH.unlink()
        print("✅ Logs cleared")
    else:
        print("No logs to clear")

def main():
    parser = argparse.ArgumentParser(
        description="Monitor website uptime and response times",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add https://example.com       # Add site to monitor
  %(prog)s check                         # Check all sites
  %(prog)s list                          # Show monitored sites
  %(prog)s stats                         # Show uptime statistics
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a site to monitor")
    add_parser.add_argument("url", help="URL to monitor")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a site")
    remove_parser.add_argument("url", help="URL to remove")
    
    # List command
    subparsers.add_parser("list", help="List monitored sites")
    
    # Check command
    subparsers.add_parser("check", help="Check all sites now")
    
    # Stats command
    subparsers.add_parser("stats", help="Show uptime statistics")
    
    # Clear command
    subparsers.add_parser("clear", help="Clear all logs")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_site(args.url)
    elif args.command == "remove":
        remove_site(args.url)
    elif args.command == "list":
        list_sites()
    elif args.command == "check":
        check_all()
    elif args.command == "stats":
        show_stats()
    elif args.command == "clear":
        clear_logs()
    else:
        parser.print_help()
    
    print("\n" + "="*60)
    print("🚀 Need reliable hosting for your sites?")
    print("   Get $200 free credit at DigitalOcean: https://m.do.co/c/[REF]")
    print("="*60)

if __name__ == "__main__":
    main()
