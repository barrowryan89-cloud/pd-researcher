#!/usr/bin/env python3
"""
net_info_free.py - Network Information
Show network interfaces, IP addresses, and connection info.
Zero dependencies. Pure Python 3.
"""

import sys
import socket
import subprocess

def get_hostname() -> str:
    """Get system hostname."""
    return socket.gethostname()

def get_public_ip() -> str:
    """Try to get public IP."""
    try:
        # Try multiple services
        services = [
            ('ifconfig.me', 80, b'GET /ip HTTP/1.1\r\nHost: ifconfig.me\r\n\r\n'),
        ]
        
        for host, port, request in services:
            try:
                sock = socket.create_connection((host, port), timeout=3)
                sock.send(request)
                response = sock.recv(4096).decode()
                sock.close()
                
                # Extract IP from response
                lines = response.split('\r\n')
                body_start = False
                for line in lines:
                    if body_start and line.strip():
                        ip = line.strip()
                        if '.' in ip and len(ip) < 16:
                            return ip
                    if line == '':
                        body_start = True
            except:
                continue
        
        return None
    except:
        return None

def get_local_ips():
    """Get local IP addresses."""
    ips = []
    try:
        # Get hostname's IP
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
            if ip != '127.0.0.1':
                ips.append(('Hostname', ip))
        except:
            pass
        
        # Try to get all interfaces using various methods
        try:
            # Try using ip command
            result = subprocess.run(
                ['ip', 'addr', 'show'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and '127.0.0.1' not in line:
                        parts = line.strip().split()
                        for i, part in enumerate(parts):
                            if part == 'inet':
                                ip_with_mask = parts[i + 1]
                                ip = ip_with_mask.split('/')[0]
                                # Get interface name from previous line
                                ips.append(('Network', ip))
                                break
        except:
            pass
        
        # Fallback: try to connect to external host to determine local IP
        if not ips:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.connect(('8.8.8.8', 80))
                local_ip = sock.getsockname()[0]
                sock.close()
                ips.append(('Primary', local_ip))
            except:
                pass
        
    except Exception as e:
        pass
    
    return ips

def get_dns_servers():
    """Try to get DNS servers."""
    dns_servers = []
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    parts = line.split()
                    if len(parts) >= 2:
                        dns_servers.append(parts[1])
    except:
        pass
    return dns_servers

def get_default_gateway():
    """Try to get default gateway."""
    try:
        result = subprocess.run(
            ['ip', 'route', 'show', 'default'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'default via' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'via':
                            return parts[i + 1]
    except:
        pass
    return None

def show_network_info():
    """Display network information."""
    print("🌐 Network Information")
    print("=" * 60)
    
    # Hostname
    hostname = get_hostname()
    print(f"\n💻 Hostname: {hostname}")
    
    # Local IPs
    print(f"\n📍 Local IP Addresses:")
    local_ips = get_local_ips()
    if local_ips:
        # Remove duplicates while preserving order
        seen = set()
        for source, ip in local_ips:
            if ip not in seen:
                print(f"  {ip}")
                seen.add(ip)
    else:
        print("  Unable to determine")
    
    # Public IP
    print(f"\n🌍 Public IP:")
    public_ip = get_public_ip()
    if public_ip:
        print(f"  {public_ip}")
    else:
        print("  Unable to determine (no internet connection)")
    
    # Default Gateway
    gateway = get_default_gateway()
    if gateway:
        print(f"\n🚪 Default Gateway: {gateway}")
    
    # DNS Servers
    dns = get_dns_servers()
    if dns:
        print(f"\n🔍 DNS Servers:")
        for server in dns[:3]:
            print(f"  {server}")
    
    # Connection test
    print(f"\n📡 Connection Test:")
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=3)
        print("  ✅ Internet connection active")
    except:
        print("  ❌ No internet connection")
    
    print("\n" + "=" * 60)

def main():
    show_network_info()

if __name__ == "__main__":
    main()
