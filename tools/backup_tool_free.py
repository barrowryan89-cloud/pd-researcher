#!/usr/bin/env python3
"""
Backup Tool - Free Tool
Simple file/directory backup
Free version: Single backup to local directory
Paid upgrade: Remote backup (S3, Drive), compression, encryption, schedule

Usage: python3 backup_tool_free.py <source> <destination>
"""

import sys
import os
import shutil
import datetime

def create_backup(source, dest_dir):
    """Create backup of source"""
    if not os.path.exists(source):
        return {'error': f'Source not found: {source}'}
    
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
        except Exception as e:
            return {'error': f'Could not create destination: {e}'}
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    basename = os.path.basename(source.rstrip(os.sep))
    dest_name = f"{basename}_{timestamp}"
    dest_path = os.path.join(dest_dir, dest_name)
    
    try:
        if os.path.isfile(source):
            shutil.copy2(source, dest_path)
        else:
            shutil.copytree(source, dest_path)
        return {'status': 'success', 'path': dest_path}
    except Exception as e:
        return {'error': str(e)}

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                    BACKUP TOOL v1.0                        ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Create local backups of files and directories             ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Cloud backup (S3, Google Drive, Dropbox)             ║
║     → Automatic scheduling (cron integration)              ║
║     → Compression (zip, tar.gz)                            ║
║     → Encryption (AES-256)                                 ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 3:
        print("❌ Missing arguments.")
        print("\nUsage:")
        print("  python3 backup_tool_free.py project/ backups/")
        print("  python3 backup_tool_free.py important.txt backups/")
        sys.exit(1)
    
    source = sys.argv[1]
    dest = sys.argv[2]
    
    print(f"🔄 Backing up: {source}")
    print(f"   To: {dest}\n")
    
    result = create_backup(source, dest)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"✅ BACKUP COMPLETE")
    print(f"{'='*60}\n")
    
    print(f"Location: {result['path']}")
    
    print(f"\n{'='*60}")
    print("\n💡 Want cloud backup and encryption?")
    print("   Upgrade to PD_Researcher v1 for secure automated backups")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("\n☁️  Cloud Backup Recommendation:")
    print("   Sync your backups to the cloud with Backblaze")
    print("   Unlimited personal backup: $7/month")
    print("   https://www.backblaze.com/cloud-backup.html")
    print("="*60)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
