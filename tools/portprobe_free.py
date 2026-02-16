#!/usr/bin/env python3
"""
PortProbe - Free CLI Tool #37
Check port availability, scan ranges, detect services
Zero dependencies, single file, MIT licensed
https://github.com/barrowryan89-cloud/pd-researcher
"""

import socket
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

__version__ = "1.0.0"

def check_port(host, port, timeout=2):
    """Check if a single port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return port, result == 0
    except socket.gaierror:
        return port, None
    except Exception:
        return port, False

def scan_port_range(host, start_port, end_port, max_workers=50, timeout=2):
    """Scan a range of ports concurrently."""
    open_ports = []
    closed_ports = []
    errors = []
    
    print(f"🔍 Scanning {host}:{start_port}-{end_port} ({end_port - start_port + 1} ports)...")
    print(f"⚡ Using {max_workers} workers, {timeout}s timeout\n")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(check_port, host, port, timeout): port 
            for port in range(start_port, end_port + 1)
        }
        
        for future in as_completed(futures):
            port, is_open = future.result()
            
            if is_open is None:
                errors.append(port)
            elif is_open:
                open_ports.append(port)
                service = get_common_service(port)
                print(f"✅ Port {port}/tcp OPEN - {service}")
            # Don't print closed ports to reduce noise
    
    elapsed = time.time() - start_time
    
    return open_ports, closed_ports, errors, elapsed

def get_common_service(port):
    """Return common service name for well-known ports."""
    services = {
        20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet",
        25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3",
        143: "IMAP", 443: "HTTPS", 465: "SMTPS", 587: "SMTP-Submission",
        993: "IMAPS", 995: "POP3S", 3306: "MySQL", 5432: "PostgreSQL",
        6379: "Redis", 27017: "MongoDB", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
        3000: "React/Dev", 5000: "Flask", 8000: "Django/Dev", 9000: "Portainer/PHP-FPM"
    }
    return services.get(port, "Unknown")

def quick_check(host, ports):
    """Quick check specific ports."""
    results = []
    print(f"🔍 Quick checking {host}...\n")
    
    for port in ports:
        port_num, is_open = check_port(host, port)
        service = get_common_service(port_num)
        
        if is_open:
            status = "✅ OPEN"
        elif is_open is None:
            status = "❌ ERROR"
        else:
            status = "❌ CLOSED"
        
        results.append((port_num, is_open, service))
        print(f"{status:12} {port_num:5}/tcp - {service}")
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description="PortProbe - Fast port scanner with zero dependencies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -H localhost -p 22,80,443      Quick check specific ports
  %(prog)s -H 192.168.1.1 -r 1-1000       Scan port range
  %(prog)s -H example.com --common        Check common service ports
  %(prog)s -H 10.0.0.5 -r 8000-9000 -w 100  Fast scan with 100 workers
        """
    )
    
    parser.add_argument("-H", "--host", required=True, help="Target host/IP to scan")
    parser.add_argument("-p", "--ports", help="Comma-separated ports (e.g., 22,80,443)")
    parser.add_argument("-r", "--range", help="Port range (e.g., 1-1000)")
    parser.add_argument("--common", action="store_true", help="Check common service ports")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Concurrent workers (default: 50)")
    parser.add_argument("-t", "--timeout", type=float, default=2.0, help="Timeout seconds (default: 2)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    # Validate input
    if not any([args.ports, args.range, args.common]):
        parser.error("Must specify one of: --ports, --range, or --common")
    
    print(f"""
╔═══════════════════════════════════════╗
║  PortProbe v{__version__} - Free CLI Tool #37     ║
║  https://pd-researcher.agent          ║
╚═══════════════════════════════════════╝
""")
    
    # Common ports
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 
                    3000, 3306, 5432, 6379, 8000, 8080, 8443, 9000, 27017]
    
    try:
        if args.ports:
            ports = [int(p.strip()) for p in args.ports.split(",")]
            results = quick_check(args.host, ports)
            open_count = sum(1 for _, is_open, _ in results if is_open)
            print(f"\n📊 Results: {open_count}/{len(ports)} ports open")
            
        elif args.common:
            results = quick_check(args.host, common_ports)
            open_count = sum(1 for _, is_open, _ in results if is_open)
            print(f"\n📊 Results: {open_count}/{len(common_ports)} common ports open")
            
        elif args.range:
            try:
                start, end = map(int, args.range.split("-"))
                if start < 1 or end > 65535 or start > end:
                    print("❌ Invalid range. Use 1-65535, start < end")
                    sys.exit(1)
                
                open_ports, closed, errors, elapsed = scan_port_range(
                    args.host, start, end, args.workers, args.timeout
                )
                
                print(f"\n{'='*50}")
                print(f"📊 SCAN COMPLETE")
                print(f"{'='*50}")
                print(f"Open ports:   {len(open_ports)}")
                if open_ports:
                    print(f"Port list:    {', '.join(map(str, sorted(open_ports)))}")
                print(f"Scan time:    {elapsed:.2f}s")
                print(f"Rate:         {(end - start + 1) / elapsed:.0f} ports/sec")
                
            except ValueError:
                print("❌ Invalid range format. Use: start-end (e.g., 1-1000)")
                sys.exit(1)
        
        print(f"\n💡 Upgrade to PD_Researcher Pro for:")
        print(f"   • Service version detection")
        print(f"   • OS fingerprinting")
        print(f"   • Export to JSON/CSV")
        print(f"   • https://pd-researcher.agent")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
