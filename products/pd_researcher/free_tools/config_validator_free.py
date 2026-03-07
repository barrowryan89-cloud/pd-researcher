#!/usr/bin/env python3
"""
🔧 Config Validator Free — Validate config files (JSON, YAML, ENV)
Check syntax, schema compliance, and common misconfigurations

FREE VERSION: Basic validation
PAID UPGRADE: PD_Researcher v1 — Custom schema rules, CI/CD integration, auto-fix
Upgrade: Send $29 in SOL/USDC to: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ
"""

import sys
import json
import re
import argparse
from pathlib import Path

VERSION = "1.0.0"
PAYMENT_ADDRESS = "FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════╗
║             🔧 CONFIG VALIDATOR FREE v1.0                  ║
║         Validate JSON, YAML, ENV, and more                ║
╠═══════════════════════════════════════════════════════════╣
║  Check syntax, find errors, ensure valid configurations   ║
║  💎 Upgrade: PD_Researcher v1 for CI/CD integration       ║
╚═══════════════════════════════════════════════════════════╝
    """)

def print_upgrade_cta():
    print(f"""
┌─────────────────────────────────────────────────────────────┐
│ 💎 WANT MORE POWER?                                          │
│                                                              │
│   PD_Researcher v1 includes:                                 │
│   • Custom JSON Schema validation                            │
│   • YAML anchor/reference checking                           │
│   • .env file cross-reference validation                     │
│   • CI/CD pipeline integration (GitHub Actions, etc)         │
│   • Auto-fix suggestions & patches                           │
│   • Docker Compose / Kubernetes validation                   │
│                                                              │
│   Upgrade: Send $29 in SOL/USDC to:                          │
│   {PAYMENT_ADDRESS}     │
│                                                              │
│   Then email screenshot to: devilliers.cody@gmail.com        │
└─────────────────────────────────────────────────────────────┘
    """)

def detect_format(filepath):
    """Detect configuration file format from extension."""
    ext = Path(filepath).suffix.lower()
    format_map = {
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.env': 'env',
        '.ini': 'ini',
        '.toml': 'toml',
        '.conf': 'conf',
        '.cfg': 'ini',
        '.properties': 'properties',
    }
    return format_map.get(ext, 'unknown')

def validate_json(filepath):
    """Validate JSON file."""
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'valid': False, 'errors': [str(e)], 'warnings': []}
    
    # Check for common issues
    if content.strip().startswith('//'):
        errors.append("JSON does not support // comments")
    
    if re.search(r',\s*[}\]]', content):
        warnings.append("Trailing commas detected (not valid in strict JSON)")
    
    # Try to parse
    try:
        data = json.loads(content)
        
        # Check for common schema issues
        if isinstance(data, dict):
            for key in data.keys():
                if ' ' in key:
                    warnings.append(f"Key '{key}' contains spaces")
                if key != key.strip():
                    warnings.append(f"Key '{key}' has leading/trailing whitespace")
        
        return {
            'valid': True,
            'errors': errors,
            'warnings': warnings,
            'type': type(data).__name__,
            'keys': len(data) if isinstance(data, dict) else None,
            'items': len(data) if isinstance(data, list) else None
        }
    except json.JSONDecodeError as e:
        errors.append(f"JSON parse error: {e}")
        return {'valid': False, 'errors': errors, 'warnings': warnings}

def validate_yaml(filepath):
    """Basic YAML validation without external deps."""
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return {'valid': False, 'errors': [str(e)], 'warnings': []}
    
    indent_stack = [0]
    in_multiline = False
    
    for i, line in enumerate(lines, 1):
        # Skip empty lines and comments
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            continue
        
        # Check indentation
        indent = len(line) - len(stripped)
        
        if not in_multiline:
            # Check for mixed tabs/spaces
            if '\t' in line[:indent] and ' ' in line[:indent]:
                errors.append(f"Line {i}: Mixed tabs and spaces in indentation")
            
            # Check indentation consistency
            if indent > indent_stack[-1]:
                if indent - indent_stack[-1] != 2 and indent - indent_stack[-1] != 4:
                    warnings.append(f"Line {i}: Unusual indentation (not 2 or 4 spaces)")
                indent_stack.append(indent)
            while indent < indent_stack[-1]:
                indent_stack.pop()
            
            if indent not in indent_stack:
                errors.append(f"Line {i}: Inconsistent indentation")
        
        # Check for multiline strings
        if stripped.endswith('|') or stripped.endswith('>'):
            in_multiline = True
        elif in_multiline and stripped:
            in_multiline = False
        
        # Check for common issues
        if ': ' not in stripped and stripped.endswith(':'):
            # Key with no value
            pass
        elif ': ' not in stripped and not stripped.startswith('-'):
            if '=' not in stripped:
                warnings.append(f"Line {i}: Possibly malformed (no colon or dash)")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'lines': len(lines)
    }

def validate_env(filepath):
    """Validate .env file."""
    errors = []
    warnings = []
    defined_vars = set()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return {'valid': False, 'errors': [str(e)], 'warnings': []}
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            continue
        
        # Check format
        if '=' not in stripped:
            errors.append(f"Line {i}: Missing '=' in variable assignment")
            continue
        
        key, _, value = stripped.partition('=')
        key = key.strip()
        
        # Check key validity
        if ' ' in key:
            errors.append(f"Line {i}: Variable name '{key}' contains spaces")
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
            warnings.append(f"Line {i}: Variable name '{key}' may not be valid")
        
        # Check for duplicates
        if key in defined_vars:
            warnings.append(f"Line {i}: Variable '{key}' redefined")
        defined_vars.add(key)
        
        # Security checks
        if any(s in key.lower() for s in ['password', 'secret', 'key', 'token']):
            if value.strip() in ('', '""', "''"):
                warnings.append(f"Line {i}: '{key}' appears to be empty")
            if len(value) < 8 and value.strip() not in ('', '""', "''"):
                warnings.append(f"Line {i}: '{key}' value seems short")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'variables': len(defined_vars),
        'lines': len(lines)
    }

def validate_file(filepath, format_type=None):
    """Validate a configuration file."""
    print(f"\n📁 Validating: {filepath}\n")
    
    if not format_type:
        format_type = detect_format(filepath)
    
    print(f"   Detected format: {format_type.upper()}")
    print(f"   {'─' * 50}")
    
    validators = {
        'json': validate_json,
        'yaml': validate_yaml,
        'yml': validate_yaml,
        'env': validate_env,
    }
    
    validator = validators.get(format_type)
    if not validator:
        print(f"   ⚠️  No validator available for '{format_type}' format")
        print(f"   Supported formats: json, yaml, yml, env")
        return
    
    result = validator(filepath)
    
    # Print results
    status = "✅ VALID" if result['valid'] else "❌ INVALID"
    print(f"\n   Status: {status}")
    
    if 'type' in result:
        print(f"   Type: {result['type']}")
    if result.get('keys'):
        print(f"   Keys: {result['keys']}")
    if result.get('items'):
        print(f"   Items: {result['items']}")
    if result.get('variables'):
        print(f"   Variables: {result['variables']}")
    if result.get('lines'):
        print(f"   Lines: {result['lines']}")
    
    if result['errors']:
        print(f"\n   ❌ ERRORS ({len(result['errors'])}):")
        for error in result['errors'][:5]:
            print(f"      • {error}")
        if len(result['errors']) > 5:
            print(f"      ... and {len(result['errors']) - 5} more")
    
    if result['warnings']:
        print(f"\n   ⚠️  WARNINGS ({len(result['warnings'])}):")
        for warning in result['warnings'][:5]:
            print(f"      • {warning}")
        if len(result['warnings']) > 5:
            print(f"      ... and {len(result['warnings']) - 5} more")
    
    print(f"\n   {'─' * 50}")
    print(f"   Total issues: {len(result['errors'])} errors, {len(result['warnings'])} warnings")

def main():
    parser = argparse.ArgumentParser(
        description='🔧 Config Validator Free — Validate config files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s config.json              # Validate JSON file
  %(prog)s .env                     # Validate environment file
  %(prog)s app.yaml --format yaml   # Force YAML format

Supported formats: json, yaml, yml, env

Upgrade to PD_Researcher v1:
  Send $29 in SOL/USDC to: {PAYMENT_ADDRESS}
        """
    )
    
    parser.add_argument('config', help='Path to config file to validate')
    parser.add_argument('--format', '-f', choices=['json', 'yaml', 'yml', 'env'],
                        help='Force specific format (auto-detect if omitted)')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {VERSION}')
    
    args = parser.parse_args()
    
    print_banner()
    validate_file(args.config, format_type=args.format)
    print_upgrade_cta()

if __name__ == '__main__':
    main()
