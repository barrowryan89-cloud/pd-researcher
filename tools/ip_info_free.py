#!/usr/bin/env python3
"""
IP Info - Free Tool
Get information about IP addresses (public, local, geolocation hints)
Free version: Basic IP info
Paid upgrade: Full geolocation, threat intelligence, bulk lookup

Usage: python3 ip_info_free.py [ip_address]
"""

import sys
import socket
import urllib.request
import json

def get_public_ip():
    """Get public IP address"""
    try:
        with urllib.request.urlopen('https://api.ipify.org?format=json', timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get('ip')
    except:
        return None

def get_local_ips():
    """Get local IP addresses"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return hostname, local_ip
    except:
        return None, None

def ip_info(ip):
    """Get basic IP info"""
    try:
        # Simple classification
        parts = ip.split('.')
        if len(parts) == 4:
            first_octet = int(parts[0])
            
            # Private ranges
            if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
                if ip.startswith('172.'):
                    second = int(parts[1])
                    if 16 <= second <= 31:
                        return 'Private (RFC1918)'
                else:
                    return 'Private (RFC1918)'
            
            # Loopback
            if ip.startswith('127.'):
                return 'Loopback'
            
            # Link-local
            if ip.startswith('169.254.'):
                return 'Link-local (APIPA)'
            
            # Multicast
            if 224 <= first_octet <= 239:
                return 'Multicast'
            
            return 'Public'
    except:
        pass
    
    return 'Unknown'

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                      IP INFO v1.0                          ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Get information about IP addresses and network setup      ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Full geolocation data                                ║
║     → ISP and ASN information                              ║
║     → Threat intelligence (is it a VPN/proxy?)             ║
║     → Bulk IP lookup                                       ║
║     → Historical data                                      ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    # Get local info
    hostname, local_ip = get_local_ips()
    
    if len(sys.argv) > 1:
        ip = sys.argv[1]
        info = ip_info(ip)
        
        print(f"{'='*60}")
        print(f"📊 IP INFORMATION")
        print(f"{'='*60}")
        print(f"\nIP Address: {ip}")
        print(f"Type: {info}")
        
        try:
            # Try reverse DNS
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"Hostname: {hostname}")
        except:
            pass
    else:
        # Show all info
        public_ip = get_public_ip()
        
        print(f"{'='*60}")
        print(f"📊 NETWORK INFORMATION")
        print(f"{'='*60}")
        
        if hostname and local_ip:
            print(f"\n🖥️  Local Machine:")
            print(f"   Hostname: {hostname}")
            print(f"   Local IP: {local_ip}")
        
        if public_ip:
            print(f"\n🌐 Public IP:")
            print(f"   {public_ip}")
            print(f"   Type: {ip_info(public_ip)}")
        else:
            print(f"\n🌐 Public IP: Could not determine")
    
    print(f"\n{'='*60}")
    print("\n💡 Want full geolocation and threat intelligence?")
    print("   Upgrade to PD_Researcher v1 for advanced IP tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
