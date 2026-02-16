#!/usr/bin/env python3
"""
Tool #35: System Info
Display system information (OS, CPU, memory, disk)
"""

import platform
import os
import sys


def get_size(bytes_size):
    """Convert bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"


def get_system_info():
    """Gather system information."""
    info = {}
    
    # Platform info
    info['os'] = platform.system()
    info['os_release'] = platform.release()
    info['os_version'] = platform.version()
    info['architecture'] = platform.architecture()[0]
    info['machine'] = platform.machine()
    info['processor'] = platform.processor() or "Unknown"
    info['hostname'] = platform.node()
    info['python_version'] = platform.python_version()
    
    # Linux-specific: read from /proc
    if info['os'] == 'Linux':
        # CPU info
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        info['cpu_model'] = line.split(':')[1].strip()
                        break
        except:
            info['cpu_model'] = info['processor']
        
        # CPU count
        info['cpu_count'] = os.cpu_count()
        
        # Memory info
        try:
            with open('/proc/meminfo', 'r') as f:
                mem_data = f.read()
                total_match = [l for l in mem_data.split('\n') if 'MemTotal' in l]
                free_match = [l for l in mem_data.split('\n') if 'MemAvailable' in l or 'MemFree' in l]
                if total_match:
                    kb = int(total_match[0].split()[1])
                    info['memory_total'] = get_size(kb * 1024)
                if free_match:
                    kb = int(free_match[0].split()[1])
                    info['memory_free'] = get_size(kb * 1024)
        except:
            info['memory_total'] = "Unknown"
            info['memory_free'] = "Unknown"
        
        # Disk usage
        try:
            stat = os.statvfs('/')
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            info['disk_total'] = get_size(total)
            info['disk_used'] = get_size(used)
            info['disk_free'] = get_size(free)
            info['disk_percent'] = f"{(used/total)*100:.1f}%"
        except:
            info['disk_total'] = "Unknown"
    
    return info


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 system_info_free.py")
        print("Display system information including OS, CPU, memory, and disk usage.")
        sys.exit(0)
    
    info = get_system_info()
    
    print("=" * 50)
    print("SYSTEM INFORMATION")
    print("=" * 50)
    print()
    print(f"Hostname:       {info.get('hostname', 'N/A')}")
    print(f"OS:             {info.get('os', 'N/A')} {info.get('os_release', '')}")
    print(f"Architecture:   {info.get('architecture', 'N/A')}")
    print(f"Machine:        {info.get('machine', 'N/A')}")
    print()
    print(f"Python:         {info.get('python_version', 'N/A')}")
    print()
    print(f"CPU:            {info.get('cpu_model', info.get('processor', 'N/A'))}")
    if 'cpu_count' in info:
        print(f"CPU Cores:      {info['cpu_count']}")
    print()
    
    if 'memory_total' in info:
        print(f"Memory Total:   {info['memory_total']}")
    if 'memory_free' in info:
        print(f"Memory Free:    {info['memory_free']}")
    print()
    
    if 'disk_total' in info:
        print(f"Disk Total:     {info['disk_total']}")
        print(f"Disk Used:      {info['disk_used']} ({info.get('disk_percent', 'N/A')})")
        print(f"Disk Free:      {info['disk_free']}")
    
    print()
    print("=" * 50)


if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
