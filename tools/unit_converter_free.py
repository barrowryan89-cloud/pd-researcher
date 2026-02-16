#!/usr/bin/env python3
"""
Unit Converter - Free Tool
Convert between various units (length, weight, temperature, etc.)
Free version: Common conversions
Paid upgrade: All units, custom conversions, batch processing

Usage: python3 unit_converter_free.py <value> <from_unit> <to_unit>
"""

import sys

# Conversion factors to base units
CONVERSIONS = {
    # Length (to meters)
    'length': {
        'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000,
        'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
    },
    # Weight (to grams)
    'weight': {
        'mg': 0.001, 'g': 1, 'kg': 1000,
        'oz': 28.3495, 'lb': 453.592
    },
    # Temperature (special handling)
    'temperature': ['c', 'f', 'k'],
    # Data (to bytes)
    'data': {
        'b': 1, 'kb': 1024, 'mb': 1024**2, 'gb': 1024**3, 'tb': 1024**4
    },
    # Time (to seconds)
    'time': {
        'ms': 0.001, 's': 1, 'm': 60, 'h': 3600, 'd': 86400
    }
}

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature"""
    # Convert to Celsius first
    if from_unit == 'c':
        celsius = value
    elif from_unit == 'f':
        celsius = (value - 32) * 5/9
    elif from_unit == 'k':
        celsius = value - 273.15
    else:
        return None
    
    # Convert from Celsius to target
    if to_unit == 'c':
        return celsius
    elif to_unit == 'f':
        return (celsius * 9/5) + 32
    elif to_unit == 'k':
        return celsius + 273.15
    else:
        return None

def convert(value, from_unit, to_unit):
    """Convert between units"""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Temperature is special
    if from_unit in CONVERSIONS['temperature'] and to_unit in CONVERSIONS['temperature']:
        return convert_temperature(value, from_unit, to_unit)
    
    # Find the category
    for category, units in CONVERSIONS.items():
        if category == 'temperature':
            continue
        if from_unit in units and to_unit in units:
            # Convert to base then to target
            base_value = value * units[from_unit]
            return base_value / units[to_unit]
    
    return None

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   UNIT CONVERTER v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Convert between various units of measurement              ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → All units (currency, pressure, energy, etc.)         ║
║     → Live currency exchange rates                         ║
║     → Batch conversions from file                          ║
║     → Custom conversion formulas                           ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 4:
        print("❌ Missing arguments.")
        print("\nUsage:")
        print("  python3 unit_converter_free.py 100 cm m")
        print("  python3 unit_converter_free.py 32 f c")
        print("  python3 unit_converter_free.py 1 gb mb")
        print("\nSupported units:")
        print("  Length: mm, cm, m, km, in, ft, yd, mi")
        print("  Weight: mg, g, kg, oz, lb")
        print("  Temp: c, f, k")
        print("  Data: b, kb, mb, gb, tb")
        print("  Time: ms, s, m, h, d")
        sys.exit(1)
    
    try:
        value = float(sys.argv[1])
    except ValueError:
        print("❌ Invalid number")
        sys.exit(1)
    
    from_unit = sys.argv[2]
    to_unit = sys.argv[3]
    
    result = convert(value, from_unit, to_unit)
    
    if result is None:
        print(f"❌ Cannot convert from '{from_unit}' to '{to_unit}'")
        print("Check that both units are in the same category")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 CONVERSION RESULT")
    print(f"{'='*60}\n")
    print(f"{value} {from_unit} = {result:.6g} {to_unit}")
    
    print(f"\n{'='*60}")
    print("\n💡 Want live currency rates and more units?")
    print("   Upgrade to PD_Researcher v1 for advanced conversion tools")
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
