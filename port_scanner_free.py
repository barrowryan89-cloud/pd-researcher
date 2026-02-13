#!/usr/bin/env python3
"""
Port Scanner - Free Tool
Simple TCP port scanner for checking open ports
Free version: Single host, common ports
Paid upgrade: Full port range, SYN stealth, OS detection, service version

Usage: python3 port_scanner_free.py <host> [ports]
"""

import sys
import socket
import concurrent.futures

def check_port(host, port, timeout=2):
    """Check if a port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                # Try to get banner
                try:
                    sock.settimeout(1)
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    return True, banner[:100] if banner else ""
                except:
                    return True, ""
            return False, ""
    except Exception as e:
        return False, ""

def scan_ports(host, ports, max_workers=50):
    """Scan multiple ports concurrently"""
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(check_port, host, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                is_open, banner = future.result()
                if is_open:
                    open_ports.append((port, banner))
                    print(f"✅ Port {port} OPEN")
                    if banner:
                        print(f"   Banner: {banner}")
            except Exception as e:
                pass
    
    return sorted(open_ports)

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                    PORT SCANNER v1.0                       ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Simple TCP port scanner for checking open ports           ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Full port range (1-65535)                            ║
║     → SYN stealth scanning                                 ║
║     → Service version detection                            ║
║     → OS fingerprinting                                    ║
║     → Nmap integration                                     ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No host provided.")
        print("\nUsage:")
        print("  python3 port_scanner_free.py example.com")
        print("  python3 port_scanner_free.py 192.168.1.1")
        print("  python3 port_scanner_free.py example.com 22,80,443")
        sys.exit(1)
    
    host = sys.argv[1]
    
    # Common ports to scan
    if len(sys.argv) > 2:
        ports = [int(p.strip()) for p in sys.argv[2].split(',')]
    else:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5432, 8080, 8443]
    
    print(f"🔄 Scanning {host}...")
    print(f"Ports: {len(ports)} common ports\n")
    
    try:
        ip = socket.gethostbyname(host)
        print(f"Resolved: {ip}\n")
    except socket.gaierror:
        print(f"❌ Could not resolve {host}")
        sys.exit(1)
    
    open_ports = scan_ports(ip, ports)
    
    print(f"\n{'='*60}")
    print(f"📊 SCAN RESULTS")
    print(f"{'='*60}")
    print(f"Host: {host} ({ip})")
    print(f"Ports scanned: {len(ports)}")
    print(f"Open ports: {len(open_ports)}")
    
    if open_ports:
        print("\nOpen ports:")
        for port, banner in open_ports:
            banner_str = f" - {banner[:50]}" if banner else ""
            print(f"  {port}{banner_str}")
    else:
        print("\nNo open ports found.")
    
    print(f"\n{'='*60}")
    print("\n💡 Want full port range and SYN stealth scanning?")
    print("   Upgrade to PD_Researcher v1 for advanced scanning")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("\n🖥️  Need a VPS to scan? Deploy a $4 DigitalOcean droplet:")
    print("   https://www.digitalocean.com/?ref=pdresearcher")
    print("   (Perfect for security testing and dev servers)")
    print("="*60)

if __name__ == "__main__":
    main()
