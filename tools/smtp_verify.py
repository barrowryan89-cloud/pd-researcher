#!/usr/bin/env python3
"""
smtp_verify - Email SMTP configuration validator
Quickly test SMTP settings without sending actual emails.

Part of the PD Researcher Free Tool Suite
"""

import argparse
import socket
import ssl
import sys
from typing import Optional, Tuple


def test_smtp_connection(
    host: str,
    port: int,
    use_tls: bool = True,
    timeout: int = 10
) -> Tuple[bool, str]:
    """
    Test SMTP server connectivity and report capabilities.
    
    Returns: (success: bool, message: str)
    """
    try:
        # Create socket
        sock = socket.create_connection((host, port), timeout=timeout)
        
        # Wrap with SSL if TLS requested and port is 465
        if use_tls and port == 465:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        
        # Receive greeting
        sock.settimeout(timeout)
        greeting = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        
        if not greeting.startswith('220'):
            sock.close()
            return False, f"Invalid greeting: {greeting}"
        
        # Send EHLO
        sock.sendall(b'EHLO smtp_verify\r\n')
        response = sock.recv(2048).decode('utf-8', errors='ignore')
        
        # Parse capabilities
        capabilities = []
        for line in response.split('\r\n'):
            if line.startswith('250-'):
                cap = line[4:].strip()
                if cap and cap != 'smtp_verify':
                    capabilities.append(cap)
        
        # Try STARTTLS if available and not already encrypted
        supports_starttls = any('STARTTLS' in cap for cap in capabilities)
        
        if supports_starttls and port != 465:
            sock.sendall(b'STARTTLS\r\n')
            tls_response = sock.recv(1024).decode('utf-8', errors='ignore')
            
            if tls_response.startswith('220'):
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
                tls_active = True
            else:
                tls_active = False
        else:
            tls_active = port == 465
        
        # Send QUIT
        sock.sendall(b'QUIT\r\n')
        sock.close()
        
        # Build result message
        status = "✅ CONNECTED"
        cap_str = ", ".join(capabilities[:5]) if capabilities else "None"
        if len(capabilities) > 5:
            cap_str += f" (+{len(capabilities)-5} more)"
        
        tls_status = "🔒 TLS Active" if tls_active else "⚠️  No TLS" if port != 465 else "🔒 Implicit TLS"
        starttls_status = "🚀 STARTTLS Available" if supports_starttls and port != 465 else ""
        
        message = f"{status}\n   Server: {greeting[:60]}{'...' if len(greeting) > 60 else ''}\n   Capabilities: {cap_str}\n   {tls_status}"
        if starttls_status:
            message += f"\n   {starttls_status}"
        
        return True, message
        
    except socket.timeout:
        return False, "❌ TIMEOUT - Server not responding"
    except socket.gaierror:
        return False, "❌ DNS ERROR - Cannot resolve hostname"
    except ConnectionRefusedError:
        return False, "❌ REFUSED - Connection rejected"
    except ssl.SSLError as e:
        return False, f"❌ TLS ERROR - {str(e)[:50]}"
    except Exception as e:
        return False, f"❌ ERROR - {str(e)[:60]}"


def main():
    parser = argparse.ArgumentParser(
        description="SMTP configuration validator - Test email server settings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smtp_verify smtp.gmail.com 587
  smtp_verify smtp.office365.com 587 --no-tls
  smtp_verify mail.example.com 465
  smtp_verify localhost 25 --timeout 5

Common Ports:
  25   - Standard SMTP (often blocked)
  587  - Submission (STARTTLS recommended)
  465  - SMTPS (Implicit TLS)
  2525 - Alternative submission port
        """
    )
    
    parser.add_argument('host', help='SMTP server hostname')
    parser.add_argument('port', type=int, nargs='?', default=587, 
                        help='Port number (default: 587)')
    parser.add_argument('--no-tls', action='store_true',
                        help='Disable TLS/SSL (insecure, for testing only)')
    parser.add_argument('--timeout', type=int, default=10,
                        help='Connection timeout in seconds (default: 10)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    
    args = parser.parse_args()
    
    use_tls = not args.no_tls
    
    if args.json:
        import json
        success, message = test_smtp_connection(args.host, args.port, use_tls, args.timeout)
        result = {
            "host": args.host,
            "port": args.port,
            "success": success,
            "message": message.replace('✅ ', '').replace('❌ ', '').replace('🔒 ', '').replace('⚠️  ', '').replace('🚀 ', ''),
            "tls_enabled": use_tls
        }
        print(json.dumps(result, indent=2))
        sys.exit(0 if success else 1)
    else:
        print(f"🔍 Testing {args.host}:{args.port}...")
        print(f"   TLS: {'Enabled' if use_tls else 'Disabled'}")
        print()
        
        success, message = test_smtp_connection(args.host, args.port, use_tls, args.timeout)
        print(message)
        
        print()
        if success:
            print("✨ SMTP server is reachable and responding correctly")
        else:
            print("💡 Tip: Check firewall rules and verify the server address")
        
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
