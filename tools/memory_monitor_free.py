#!/usr/bin/env python3
"""
Memory Monitor - Free Tool
Monitor system memory usage in real-time
Free version: Single snapshot
Paid upgrade: Continuous monitoring, alerts, logging, process-level detail

Usage: python3 memory_monitor_free.py
"""

import sys
import os

def get_memory_info():
    """Get memory information from /proc/meminfo"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        mem_info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                # Extract number from value like "8192000 kB"
                num = ''.join(filter(str.isdigit, value))
                mem_info[key.strip()] = int(num) if num else 0
        
        return mem_info
    except Exception as e:
        return None

def format_kb(kb):
    """Format kilobytes to human readable"""
    mb = kb / 1024
    gb = mb / 1024
    
    if gb >= 1:
        return f"{gb:.2f} GB"
    else:
        return f"{mb:.2f} MB"

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   MEMORY MONITOR v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Monitor system memory usage                               ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Real-time continuous monitoring                      ║
║     → Memory usage alerts                                  ║
║     → Process-level memory tracking                        ║
║     → Historical logging and graphs                        ║
║     → Memory leak detection                                ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    mem_info = get_memory_info()
    
    if not mem_info:
        print("❌ Could not read memory information.")
        print("   This tool works on Linux systems with /proc/meminfo")
        sys.exit(1)
    
    total = mem_info.get('MemTotal', 0)
    free = mem_info.get('MemFree', 0)
    available = mem_info.get('MemAvailable', free)
    buffers = mem_info.get('Buffers', 0)
    cached = mem_info.get('Cached', 0)
    
    used = total - available
    used_percent = (used / total * 100) if total > 0 else 0
    
    print(f"{'='*60}")
    print(f"📊 MEMORY STATUS")
    print(f"{'='*60}\n")
    
    print(f"Total Memory:     {format_kb(total)}")
    print(f"Used:             {format_kb(used)} ({used_percent:.1f}%)")
    print(f"Available:        {format_kb(available)}")
    print(f"Free:             {format_kb(free)}")
    print(f"Buffers:          {format_kb(buffers)}")
    print(f"Cached:           {format_kb(cached)}")
    
    # Visual bar
    bar_width = 40
    filled = int(bar_width * used_percent / 100)
    bar = '█' * filled + '░' * (bar_width - filled)
    
    print(f"\n[{bar}] {used_percent:.1f}%")
    
    if used_percent > 90:
        print("\n🔴 WARNING: Memory usage is critical!")
    elif used_percent > 75:
        print("\n🟡 WARNING: Memory usage is high")
    else:
        print("\n🟢 Memory usage is normal")
    
    print(f"\n{'='*60}")
    print("\n💡 Want real-time monitoring and alerts?")
    print("   Upgrade to PD_Researcher v1 for advanced system monitoring")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
