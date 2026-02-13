#!/usr/bin/env python3
"""
File Splitter - Free Tool
Split large files into smaller chunks
Free version: Basic line-based splitting
Paid upgrade: Size-based, binary mode, rejoin, compression

Usage: python3 file_splitter_free.py <file> <lines_per_chunk>
"""

import sys
import os

def split_file(filepath, lines_per_chunk, prefix=None):
    """Split file into chunks"""
    if not os.path.exists(filepath):
        return {'error': f'File not found: {filepath}'}
    
    if prefix is None:
        prefix = filepath + '.part'
    
    chunk_files = []
    chunk_num = 0
    current_lines = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                current_lines.append(line)
                
                if len(current_lines) >= lines_per_chunk:
                    chunk_num += 1
                    chunk_path = f"{prefix}{chunk_num:03d}"
                    with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
                        chunk_file.writelines(current_lines)
                    chunk_files.append(chunk_path)
                    current_lines = []
            
            # Write remaining lines
            if current_lines:
                chunk_num += 1
                chunk_path = f"{prefix}{chunk_num:03d}"
                with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
                    chunk_file.writelines(current_lines)
                chunk_files.append(chunk_path)
        
        return {
            'chunks': chunk_files,
            'total_chunks': len(chunk_files),
            'original_size': os.path.getsize(filepath)
        }
    except Exception as e:
        return {'error': str(e)}

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   FILE SPLITTER v1.0                       ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Split large files into smaller chunks                     ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Split by size (MB/GB)                                ║
║     → Binary file support                                  ║
║     → Automatic rejoining                                  ║
║     → Compression (gzip)                                   ║
║     → Parallel processing                                  ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 3:
        print("❌ Missing arguments.")
        print("\nUsage:")
        print("  python3 file_splitter_free.py large_file.txt 1000")
        print("  python3 file_splitter_free.py data.csv 500")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        lines_per_chunk = int(sys.argv[2])
    except ValueError:
        print("❌ Lines per chunk must be a number")
        sys.exit(1)
    
    print(f"🔄 Splitting: {filepath}")
    print(f"   Lines per chunk: {lines_per_chunk}\n")
    
    result = split_file(filepath, lines_per_chunk)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 SPLIT COMPLETE")
    print(f"{'='*60}\n")
    
    print(f"Original file: {filepath}")
    print(f"Original size: {result['original_size']:,} bytes")
    print(f"Total chunks: {result['total_chunks']}")
    
    print(f"\nCreated files:")
    for chunk in result['chunks']:
        size = os.path.getsize(chunk)
        print(f"  {chunk} ({size:,} bytes)")
    
    print(f"\n{'='*60}")
    print("\n💡 Want size-based splitting and auto-rejoin?")
    print("   Upgrade to PD_Researcher v1 for advanced file tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("\n☁️  Cloud Storage:")
    print("   Need to store large files? Try Backblaze B2")
    print("   $0.005/GB/month — cheaper than S3")
    print("   https://www.backblaze.com/b2/cloud-storage.html")
    print("="*60)

if __name__ == "__main__":
    main()
