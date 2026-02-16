#!/usr/bin/env python3
"""
Process Monitor - Free Tool
List running processes and their resource usage
Free version: Basic process list
Paid upgrade: Real-time monitoring, filtering, killing, detailed stats

Usage: python3 process_monitor_free.py [filter]
"""

import sys
import os
import glob

def get_processes():
    """Get list of running processes from /proc"""
    processes = []
    
    try:
        for pid_str in glob.glob('/proc/[0-9]*'):
            try:
                pid = int(os.path.basename(pid_str))
                
                # Read process info
                with open(f'{pid_str}/stat', 'r') as f:
                    stat = f.read().split()
                
                with open(f'{pid_str}/comm', 'r') as f:
                    comm = f.read().strip()
                
                # Try to get command line
                try:
                    with open(f'{pid_str}/cmdline', 'r') as f:
                        cmdline = f.read().replace('\0', ' ').strip()
                        if not cmdline:
                            cmdline = f"[{comm}]"
                except:
                    cmdline = f"[{comm}]"
                
                # Get memory info
                try:
                    with open(f'{pid_str}/status', 'r') as f:
                        status_lines = f.readlines()
                    
                    vm_rss = 0
                    for line in status_lines:
                        if line.startswith('VmRSS:'):
                            vm_rss = int(line.split()[1])  # in kB
                            break
                except:
                    vm_rss = 0
                
                processes.append({
                    'pid': pid,
                    'name': comm,
                    'cmdline': cmdline[:60] + '...' if len(cmdline) > 60 else cmdline,
                    'memory_kb': vm_rss
                })
            except (PermissionError, ProcessLookupError, FileNotFoundError):
                continue
    except Exception as e:
        print(f"Error reading processes: {e}")
    
    return processes

def format_kb(kb):
    """Format kilobytes"""
    if kb >= 1024 * 1024:
        return f"{kb / (1024 * 1024):.1f}G"
    elif kb >= 1024:
        return f"{kb / 1024:.1f}M"
    else:
        return f"{kb}K"

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                  PROCESS MONITOR v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  List running processes and their resource usage           ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Real-time continuous monitoring (like htop)          ║
║     → CPU usage per process                                ║
║     → Filter by name, user, CPU, memory                    ║
║     → Kill processes                                       ║
║     → Process tree view                                    ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    filter_term = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🔄 Scanning processes...\n")
    processes = get_processes()
    
    if filter_term:
        processes = [p for p in processes if filter_term.lower() in p['name'].lower() or filter_term.lower() in p['cmdline'].lower()]
    
    # Sort by memory
    processes.sort(key=lambda x: x['memory_kb'], reverse=True)
    
    print(f"{'='*80}")
    print(f"📊 RUNNING PROCESSES ({len(processes)} total)")
    print(f"{'='*80}\n")
    
    print(f"{'PID':<10} {'MEMORY':<10} {'NAME/COMMAND':<60}")
    print("-" * 80)
    
    for proc in processes[:30]:  # Show top 30 by memory
        print(f"{proc['pid']:<10} {format_kb(proc['memory_kb']):<10} {proc['cmdline']:<60}")
    
    if len(processes) > 30:
        print(f"\n... and {len(processes) - 30} more processes")
    
    print(f"\n{'='*80}")
    print("\n💡 Want real-time monitoring and process control?")
    print("   Upgrade to PD_Researcher v1 for advanced process management")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*80)

if __name__ == "__main__":
    main()
