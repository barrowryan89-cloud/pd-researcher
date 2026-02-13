#!/usr/bin/env python3
"""
port_scan - Fast TCP port scanner for developers
Quickly check which ports are open on any host

Examples:
    port_scan example.com
    port_scan 192.168.1.1 --ports 22,80,443,8080
    port_scan server.com --range 1-1000 --timeout 0.5
    port_scan api.example.com --top --json
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime

# Top 100 most common ports (simplified top 20 for speed)
TOP_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443, 9200]

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    993: "IMAPS", 995: "POP3S", 1723: "PPTP", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB",
    6379: "Redis", 11211: "Memcached"
}

async def scan_port(host: str, port: int, timeout: float) -> tuple:
    """Scan a single port, return (port, is_open, service)"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        service = COMMON_SERVICES.get(port, "unknown")
        return (port, True, service)
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return (port, False, None)

async def scan_ports(host: str, ports: list, timeout: float, concurrency: int = 100):
    """Scan multiple ports concurrently"""
    semaphore = asyncio.Semaphore(concurrency)
    
    async def scan_with_limit(port):
        async with semaphore:
            return await scan_port(host, port, timeout)
    
    tasks = [scan_with_limit(port) for port in ports]
    return await asyncio.gather(*tasks)

def parse_ports(ports_str: str) -> list:
    """Parse port string like '80,443' or '1-100' into list of ints"""
    ports = []
    for part in ports_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports

def main():
    parser = argparse.ArgumentParser(
        description="Fast TCP port scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  port_scan example.com                    # Scan top 20 ports
  port_scan 192.168.1.1 --top              # Scan top 20 ports
  port_scan server.com --ports 22,80,443   # Scan specific ports
  port_scan api.com --range 1-1000         # Scan port range
  port_scan host.com --top --json          # JSON output
        """
    )
    parser.add_argument("host", help="Host to scan (IP or domain)")
    parser.add_argument("--ports", "-p", help="Comma-separated ports (e.g., 80,443,8080)")
    parser.add_argument("--range", "-r", help="Port range (e.g., 1-1000)")
    parser.add_argument("--top", "-t", action="store_true", help="Scan top 20 common ports")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout per port (seconds)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--concurrency", "-c", type=int, default=100, help="Max concurrent scans")
    
    args = parser.parse_args()
    
    # Determine ports to scan
    if args.ports:
        ports = parse_ports(args.ports)
    elif args.range:
        ports = parse_ports(args.range)
    else:
        ports = TOP_PORTS
    
    # Run scan
    start_time = datetime.now()
    results = asyncio.run(scan_ports(args.host, ports, args.timeout, args.concurrency))
    duration = (datetime.now() - start_time).total_seconds()
    
    # Filter open ports
    open_ports = [(p, s) for p, is_open, s in results if is_open]
    closed_count = len([r for r in results if not r[1]])
    
    if args.json:
        output = {
            "host": args.host,
            "scanned": len(ports),
            "open": len(open_ports),
            "closed": closed_count,
            "duration_seconds": round(duration, 2),
            "open_ports": [{"port": p, "service": s} for p, s in open_ports]
        }
        print(json.dumps(output, indent=2))
    else:
        # Pretty output
        print(f"\n🔍  Port Scan Results: {args.host}")
        print(f"   Scanned {len(ports)} ports in {duration:.2f}s")
        print(f"   {'─' * 40}")
        
        if open_ports:
            print(f"   🟢 OPEN PORTS ({len(open_ports)} found):")
            for port, service in sorted(open_ports):
                service_str = f" ({service})" if service != "unknown" else ""
                print(f"      ✅ {port:>5}{service_str}")
        else:
            print("   ⚪ No open ports found")
        
        print(f"   {'─' * 40}")
        print(f"   Closed: {closed_count} | Filtered/Timeout: {len(ports) - len(results)}")
        
        if open_ports:
            print(f"\n   💡 Tip: Use --json for programmatic output")
    
    return 0 if open_ports else 1

if __name__ == "__main__":
    sys.exit(main())
