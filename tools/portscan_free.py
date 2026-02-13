#!/usr/bin/env python3
"""
portscan — Quick TCP port scanner
Tool #69 — Free CLI Tool for PD Researcher
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(host, port, timeout=1):
    """Scan a single port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return port, result == 0
    except Exception:
        return port, False


def scan_ports(host, ports, timeout=1, max_workers=50):
    """Scan multiple ports concurrently."""
    open_ports = []
    closed_ports = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, host, port, timeout): port for port in ports}
        
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
            else:
                closed_ports.append(port)
    
    return sorted(open_ports), sorted(closed_ports)


def get_common_ports():
    """Get list of common ports."""
    return [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5432, 8080, 8443]


def get_service_name(port):
    """Get common service name for port."""
    services = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        465: 'SMTPS',
        587: 'SMTP (Submission)',
        993: 'IMAPS',
        995: 'POP3S',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        8080: 'HTTP-Proxy',
        8443: 'HTTPS-Alt',
    }
    return services.get(port, 'Unknown')


def main():
    parser = argparse.ArgumentParser(
        description='Quick TCP port scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  portscan example.com                      # Scan common ports
  portscan 192.168.1.1 -p 22,80,443        # Scan specific ports
  portscan server.com -p 1-1000            # Scan port range
  portscan target.com --all                # Scan top 1000 ports
        """
    )
    
    parser.add_argument('host', help='Target host/IP to scan')
    parser.add_argument('-p', '--ports',
                       help='Ports to scan (e.g., 80,443 or 1-1000)')
    parser.add_argument('--common', action='store_true',
                       help='Scan common ports (default)')
    parser.add_argument('--all', action='store_true',
                       help='Scan top 100 ports')
    parser.add_argument('-t', '--timeout', type=float, default=1.0,
                       help='Connection timeout in seconds (default: 1)')
    parser.add_argument('-w', '--workers', type=int, default=50,
                       help='Max concurrent workers (default: 50)')
    parser.add_argument('--open-only', action='store_true',
                       help='Only show open ports')
    
    args = parser.parse_args()
    
    # Determine ports to scan
    if args.ports:
        if '-' in args.ports:
            start, end = args.ports.split('-')
            ports = list(range(int(start), int(end) + 1))
        else:
            ports = [int(p) for p in args.ports.split(',')]
    elif args.all:
        ports = list(range(1, 101))  # Top 100
    else:
        ports = get_common_ports()
    
    print(f"Scanning {args.host} ({len(ports)} ports)...")
    print(f"Timeout: {args.timeout}s | Workers: {args.workers}\n")
    
    # Resolve host
    try:
        ip = socket.gethostbyname(args.host)
        print(f"Resolved: {args.host} → {ip}\n")
    except socket.gaierror:
        print(f"Error: Could not resolve {args.host}", file=sys.stderr)
        sys.exit(1)
    
    # Scan
    open_ports, closed_ports = scan_ports(ip, ports, args.timeout, args.workers)
    
    # Output
    if open_ports:
        print(f"✅ Open ports ({len(open_ports)}):")
        for port in open_ports:
            service = get_service_name(port)
            print(f"  {port}/tcp  {service}")
    else:
        print("No open ports found")
    
    if not args.open_only and closed_ports:
        print(f"\n❌ Closed ports ({len(closed_ports)}):")
        # Show first 10 closed ports
        for port in closed_ports[:10]:
            print(f"  {port}/tcp")
        if len(closed_ports) > 10:
            print(f"  ... and {len(closed_ports) - 10} more")


if __name__ == '__main__':
    main()
