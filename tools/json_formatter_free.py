#!/usr/bin/env python3
"""
JSON Formatter - Free Tool
Format and validate JSON files
Free version: Pretty print JSON
Paid upgrade: Schema validation, diff, batch processing

Usage: python3 json_formatter_free.py <file.json> or pipe JSON to it
"""

import sys
import json

def format_json(text):
    """Format JSON with indentation"""
    try:
        data = json.loads(text)
        return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {e}"

def validate_json(text):
    """Validate JSON and return stats"""
    try:
        data = json.loads(text)
        
        def count_items(obj):
            if isinstance(obj, dict):
                return sum(count_items(v) for v in obj.values()) + len(obj)
            elif isinstance(obj, list):
                return sum(count_items(item) for item in obj) + len(obj)
            else:
                return 1
        
        def get_depth(obj, level=0):
            if isinstance(obj, dict):
                return max((get_depth(v, level + 1) for v in obj.values()), default=level)
            elif isinstance(obj, list):
                return max((get_depth(item, level + 1) for item in obj), default=level)
            else:
                return level
        
        return {
            'valid': True,
            'type': type(data).__name__,
            'items': count_items(data),
            'depth': get_depth(data),
            'size': len(text)
        }
    except json.JSONDecodeError:
        return {'valid': False}

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   JSON FORMATTER v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Format and validate JSON files instantly                  ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Schema validation                                    ║
║     → JSON diff/compare                                    ║
║     → Batch file processing                                ║
║     → Minify/uglify option                                 ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def print_stats(stats):
    if stats['valid']:
        print(f"\n{'='*60}")
        print(f"📊 JSON STATS")
        print(f"{'='*60}")
        print(f"Valid: ✅ Yes")
        print(f"Type: {stats['type']}")
        print(f"Items: {stats['items']}")
        print(f"Max Depth: {stats['depth']}")
        print(f"Size: {stats['size']} bytes")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print(f"❌ Invalid JSON")
        print(f"{'='*60}")

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
    else:
        print("Reading from stdin (paste JSON, then Ctrl+D)...", file=sys.stderr)
        text = sys.stdin.read()
    
    if not text.strip():
        print("❌ No JSON provided.")
        print("\nUsage:")
        print("  python3 json_formatter_free.py data.json")
        print("  cat data.json | python3 json_formatter_free.py")
        sys.exit(1)
    
    print("🔄 Formatting...\n")
    
    formatted = format_json(text)
    print(formatted)
    
    stats = validate_json(text)
    print_stats(stats)
    
    if stats['valid']:
        print("\n💡 Want schema validation or JSON comparison?")
        print("   Upgrade to PD_Researcher v1 for advanced JSON tools")
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
