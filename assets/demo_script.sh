#!/bin/bash
# Demo script for PD_Researcher tools
# Run this to generate demo output for GIF/video creation
# Usage: ./assets/demo_script.sh

echo "================================================"
echo "  PD_Researcher — 98 CLI Tools Demo"
echo "================================================"
echo ""

cd "$(dirname "$0")/.."

# Demo 1: Password Generator
echo "🔐 PASSWORD GENERATOR"
echo "--------------------"
python3 password_gen_free.py --length 32 --count 3
echo ""

# Demo 2: JSON Formatter  
echo "📊 JSON FORMATTER"
echo "-----------------"
echo '{"name":"test","value":123,"nested":{"key":"value"}}' | python3 json_formatter_free.py
echo ""

# Demo 3: Timestamp Converter
echo "⏰ TIMESTAMP CONVERTER"
echo "----------------------"
python3 timestamp_converter_free.py --timestamp 1700000000
echo ""

# Demo 4: QR Code Generator
echo "📱 QR CODE GENERATOR"
echo "--------------------"
python3 qrcode_gen_free.py --text "https://github.com/barrowryan89-cloud/pd-researcher" --output /tmp/demo_qr.png
echo "✓ QR code saved to /tmp/demo_qr.png"
echo ""

# Demo 5: System Info
echo "💻 SYSTEM INFO"
echo "--------------"
python3 system_info_free.py
echo ""

echo "================================================"
echo "  All 98 tools available at:"
echo "  github.com/barrowryan89-cloud/pd-researcher"
echo "================================================"
