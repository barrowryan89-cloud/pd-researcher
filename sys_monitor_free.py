#!/usr/bin/env python3
"""
sys_monitor_free.py - System Monitor
Monitor CPU, memory, disk, and network usage in real-time.
Zero dependencies. Pure Python 3.
"""

import sys
import os
import time

def get_cpu_usage():
    """Get CPU usage percentage."""
    try:
        # Read /proc/stat
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        
        fields = line.split()
        if fields[0] != 'cpu':
            return None
        
        # Calculate usage
        user = int(fields[1])
        nice = int(fields[2])
        system = int(fields[3])
        idle = int(fields[4])
        iowait = int(fields[5])
        
        total = user + nice + system + idle + iowait
        used = user + nice + system
        
        return (used / total) * 100 if total > 0 else 0
    except:
        return None

def get_memory_info():
    """Get memory usage."""
    try:
        mem_info = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                key = line.split(':')[0]
                value = int(line.split()[1])
                mem_info[key] = value
        
        total = mem_info.get('MemTotal', 0)
        free = mem_info.get('MemFree', 0)
        available = mem_info.get('MemAvailable', free)
        buffers = mem_info.get('Buffers', 0)
        cached = mem_info.get('Cached', 0)
        
        used = total - available
        usage_percent = (used / total) * 100 if total > 0 else 0
        
        return {
            'total': total // 1024,  # MB
            'used': used // 1024,
            'free': available // 1024,
            'percent': usage_percent
        }
    except:
        return None

def get_disk_info():
    """Get disk usage for root filesystem."""
    try:
        stat = os.statvfs('/')
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bavail * stat.f_frsize
        used = total - free
        
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        percent = (used / total) * 100 if total > 0 else 0
        
        return {
            'total': total_gb,
            'used': used_gb,
            'free': free_gb,
            'percent': percent
        }
    except:
        return None

def get_load_average():
    """Get system load average."""
    try:
        with open('/proc/loadavg', 'r') as f:
            load = f.read().split()
        return {
            '1min': float(load[0]),
            '5min': float(load[1]),
            '15min': float(load[2])
        }
    except:
        return None

def get_process_count():
    """Count running processes."""
    try:
        count = 0
        for entry in os.listdir('/proc'):
            if entry.isdigit():
                count += 1
        return count
    except:
        return None

def format_bar(percent: float, width: int = 20) -> str:
    """Create ASCII progress bar."""
    filled = int((percent / 100) * width)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {percent:.1f}%"

def show_system_stats():
    """Display system statistics."""
    print("🖥️  System Monitor")
    print("=" * 60)
    
    # CPU
    cpu = get_cpu_usage()
    if cpu is not None:
        print(f"\n⚙️  CPU Usage: {format_bar(cpu)}")
    
    # Load Average
    load = get_load_average()
    if load:
        print(f"\n📊 Load Average:")
        print(f"   1 min:  {load['1min']:.2f}")
        print(f"   5 min:  {load['5min']:.2f}")
        print(f"   15 min: {load['15min']:.2f}")
    
    # Memory
    mem = get_memory_info()
    if mem:
        print(f"\n🧠 Memory: {format_bar(mem['percent'])}")
        print(f"   Used: {mem['used']:,} MB / {mem['total']:,} MB")
        print(f"   Free: {mem['free']:,} MB")
    
    # Disk
    disk = get_disk_info()
    if disk:
        print(f"\n💾 Disk: {format_bar(disk['percent'])}")
        print(f"   Used: {disk['used']:.1f} GB / {disk['total']:.1f} GB")
        print(f"   Free: {disk['free']:.1f} GB")
    
    # Processes
    procs = get_process_count()
    if procs:
        print(f"\n⚡ Processes: {procs} running")
    
    print("\n" + "=" * 60)

def monitor_loop(interval: int = 2):
    """Continuous monitoring mode."""
    print("🖥️  System Monitor (Press Ctrl+C to exit)")
    print("=" * 60)
    
    try:
        while True:
            # Clear screen (works on Unix-like systems)
            print('\033[2J\033[H', end='')
            
            print("🖥️  System Monitor (Press Ctrl+C to exit)")
            print("=" * 60)
            
            # CPU
            cpu = get_cpu_usage()
            if cpu is not None:
                print(f"\n⚙️  CPU Usage: {format_bar(cpu)}")
            
            # Load
            load = get_load_average()
            if load:
                print(f"\n📊 Load: {load['1min']:.2f} / {load['5min']:.2f} / {load['15min']:.2f}")
            
            # Memory
            mem = get_memory_info()
            if mem:
                print(f"\n🧠 Memory: {format_bar(mem['percent'])}")
                print(f"   {mem['used']:,} MB / {mem['total']:,} MB")
            
            # Disk
            disk = get_disk_info()
            if disk:
                print(f"\n💾 Disk: {format_bar(disk['percent'])}")
                print(f"   {disk['used']:.1f} GB / {disk['total']:.1f} GB")
            
            # Processes
            procs = get_process_count()
            if procs:
                print(f"\n⚡ Processes: {procs}")
            
            print(f"\n{'=' * 60}")
            print(f"Update: {time.strftime('%H:%M:%S')} | Refresh: {interval}s")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-l', '--loop', 'loop'):
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        monitor_loop(interval)
    else:
        show_system_stats()
        print("\nTip: Use 'sys_monitor_free.py loop' for continuous monitoring")

if __name__ == "__main__":
    main()
