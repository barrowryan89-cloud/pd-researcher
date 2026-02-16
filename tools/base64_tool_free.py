#!/usr/bin/env python3
"""
Base64 Tool - Free Tool
Encode/decode Base64 strings and files
Free version: Single operation
Paid upgrade: Batch processing, multiple encoding formats

Usage: python3 base64_tool_free.py <encode|decode> <text or file>
"""

import sys
import base64
import os

def encode_text(text):
    """Encode text to Base64"""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decode_text(text):
    """Decode Base64 to text"""
    try:
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return f"❌ Decode error: {e}"

def encode_file(filepath):
    """Encode file to Base64"""
    try:
        with open(filepath, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        return f"❌ File error: {e}"

def decode_file(text, output_path):
    """Decode Base64 to file"""
    try:
        data = base64.b64decode(text)
        with open(output_path, 'wb') as f:
            f.write(data)
        return f"✅ Saved to: {output_path}"
    except Exception as e:
        return f"❌ Decode error: {e}"

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                     BASE64 TOOL v1.0                       ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Encode/decode Base64 strings and files instantly          ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → URL-safe Base64                                      ║
║     → Base32, Base16, Base85 support                       ║
║     → Batch file processing                                ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 3:
        print("❌ Missing arguments.")
        print("\nUsage:")
        print("  python3 base64_tool_free.py encode 'Hello World'")
        print("  python3 base64_tool_free.py decode 'SGVsbG8gV29ybGQ='")
        print("  python3 base64_tool_free.py encodefile image.png")
        print("  python3 base64_tool_free.py decodefile 'SGVsbG8=' output.txt")
        sys.exit(1)
    
    operation = sys.argv[1].lower()
    input_data = sys.argv[2]
    
    print(f"🔄 {operation.upper()}...\n")
    
    if operation == 'encode':
        result = encode_text(input_data)
        print(f"📤 Encoded:\n{result}")
    
    elif operation == 'decode':
        result = decode_text(input_data)
        print(f"📥 Decoded:\n{result}")
    
    elif operation == 'encodefile':
        if not os.path.exists(input_data):
            print(f"❌ File not found: {input_data}")
            sys.exit(1)
        result = encode_file(input_data)
        print(f"📤 Base64 of {input_data}:\n{result[:200]}..." if len(result) > 200 else f"📤 Base64 of {input_data}:\n{result}")
        print(f"\n📊 Total length: {len(result)} characters")
    
    elif operation == 'decodefile':
        if len(sys.argv) < 4:
            print("❌ Missing output path for decodefile")
            sys.exit(1)
        output_path = sys.argv[3]
        result = decode_file(input_data, output_path)
        print(result)
    
    else:
        print(f"❌ Unknown operation: {operation}")
        print("Use: encode, decode, encodefile, decodefile")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("\n💡 Want more encoding formats?")
    print("   Upgrade to PD_Researcher v1 for Base32, Base85, URL-safe")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
