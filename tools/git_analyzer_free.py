#!/usr/bin/env python3
"""
git_analyzer_free.py — Analyze Git repository statistics
Extract insights from any git repo: commits, authors, churn, trends

Usage:
  python git_analyzer_free.py [path] [--days 30] [--format json]
  
Examples:
  python git_analyzer_free.py                    # Analyze current directory
  python git_analyzer_free.py /path/to/repo      # Analyze specific repo
  python git_analyzer_free.py --days 7           # Last 7 days only
  python git_analyzer_free.py --format json      # JSON output

Features:
- Total commits and file count
- Top contributors with commit counts
- Commit activity by day of week
- Code churn (insertions/deletions)
- Most changed files
- Branch summary

Zero dependencies. Pure Python 3.6+.
Part of PD's Free Developer Tools: https://barrowryan89-cloud.github.io/pd-researcher/
"""

import subprocess
import sys
import os
import re
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter

def run_git_command(args, cwd=None):
    """Run a git command and return output"""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None

def is_git_repo(path):
    """Check if path is a git repository"""
    git_dir = os.path.join(path, '.git')
    return os.path.isdir(git_dir) or run_git_command(['rev-parse', '--git-dir'], cwd=path) is not None

def get_total_commits(repo_path, since_days=None):
    """Get total commit count"""
    cmd = ['rev-list', '--count', 'HEAD']
    if since_days:
        cmd = ['rev-list', '--count', f'--since={since_days} days ago', 'HEAD']
    result = run_git_command(cmd, cwd=repo_path)
    return int(result) if result and result.isdigit() else 0

def get_contributors(repo_path, since_days=None):
    """Get list of contributors with commit counts"""
    cmd = ['shortlog', '-sn', 'HEAD']
    if since_days:
        cmd = ['shortlog', '-sn', f'--since={since_days} days ago', 'HEAD']
    result = run_git_command(cmd, cwd=repo_path)
    
    contributors = []
    if result:
        for line in result.split('\n'):
            match = re.match(r'\s*(\d+)\s+(.+)', line)
            if match:
                contributors.append({
                    'commits': int(match.group(1)),
                    'name': match.group(2).strip()
                })
    return contributors

def get_commit_activity_by_day(repo_path, since_days=30):
    """Get commit activity by day of week"""
    cmd = ['log', f'--since={since_days} days ago', '--format=%ad', '--date=format:%A']
    result = run_git_command(cmd, cwd=repo_path)
    
    if not result:
        return {}
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = Counter(result.split('\n'))
    return {day: counts.get(day, 0) for day in days}

def get_commit_activity_by_hour(repo_path, since_days=30):
    """Get commit activity by hour of day"""
    cmd = ['log', f'--since={since_days} days ago', '--format=%ad', '--date=format:%H']
    result = run_git_command(cmd, cwd=repo_path)
    
    if not result:
        return {}
    
    hours = [f"{h:02d}:00" for h in range(24)]
    counts = Counter(result.split('\n'))
    return {hour: counts.get(hour.split(':')[0], 0) for hour in hours}

def get_code_churn(repo_path, since_days=30):
    """Get code churn statistics (insertions/deletions)"""
    cmd = ['log', f'--since={since_days} days ago', '--format=', '--numstat']
    result = run_git_command(cmd, cwd=repo_path)
    
    if not result:
        return {'insertions': 0, 'deletions': 0, 'files_changed': 0}
    
    insertions = 0
    deletions = 0
    files_changed = 0
    
    for line in result.split('\n'):
        parts = line.split('\t')
        if len(parts) >= 2:
            try:
                ins = parts[0] if parts[0] != '-' else 0
                dels = parts[1] if parts[1] != '-' else 0
                insertions += int(ins)
                deletions += int(dels)
                files_changed += 1
            except ValueError:
                pass
    
    return {
        'insertions': insertions,
        'deletions': deletions,
        'files_changed': files_changed
    }

def get_most_changed_files(repo_path, since_days=30, limit=10):
    """Get most frequently changed files"""
    cmd = ['log', f'--since={since_days} days ago', '--format=', '--name-only']
    result = run_git_command(cmd, cwd=repo_path)
    
    if not result:
        return []
    
    files = [f.strip() for f in result.split('\n') if f.strip() and not f.strip().startswith('commit ')]
    counts = Counter(files)
    return [{'file': f, 'changes': c} for f, c in counts.most_common(limit)]

def get_branch_info(repo_path):
    """Get branch information"""
    # Current branch
    current = run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo_path)
    
    # All branches
    branches_output = run_git_command(['branch', '-a'], cwd=repo_path)
    branches = []
    if branches_output:
        for line in branches_output.split('\n'):
            branch = line.strip().strip('*').strip()
            if branch:
                branches.append(branch)
    
    return {
        'current': current or 'unknown',
        'total': len(branches),
        'branches': branches[:20]  # Limit output
    }

def get_file_count(repo_path):
    """Get total tracked file count"""
    result = run_git_command(['ls-files'], cwd=repo_path)
    if result:
        return len(result.split('\n'))
    return 0

def get_repo_size(repo_path):
    """Get repository size"""
    try:
        git_dir = os.path.join(repo_path, '.git')
        if os.path.isdir(git_dir):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(git_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            
            # Convert to human readable
            for unit in ['B', 'KB', 'MB', 'GB']:
                if total_size < 1024:
                    return f"{total_size:.1f} {unit}"
                total_size /= 1024
            return f"{total_size:.1f} TB"
    except Exception:
        pass
    return "unknown"

def get_last_commit_info(repo_path):
    """Get information about the last commit"""
    cmd = ['log', '-1', '--format=%H|%an|%ae|%ad|%s', '--date=iso']
    result = run_git_command(cmd, cwd=repo_path)
    
    if result:
        parts = result.split('|', 4)
        if len(parts) >= 5:
            return {
                'hash': parts[0][:8],
                'author': parts[1],
                'email': parts[2],
                'date': parts[3],
                'message': parts[4][:80] + ('...' if len(parts[4]) > 80 else '')
            }
    return None

def analyze_repo(repo_path, since_days=None, output_format='text'):
    """Main analysis function"""
    if not is_git_repo(repo_path):
        print(f"Error: {repo_path} is not a git repository")
        sys.exit(1)
    
    # Gather data
    data = {
        'repository': os.path.abspath(repo_path),
        'analyzed_at': datetime.now().isoformat(),
        'period_days': since_days or 'all time',
        'summary': {
            'total_commits': get_total_commits(repo_path, since_days),
            'tracked_files': get_file_count(repo_path),
            'repo_size': get_repo_size(repo_path),
            'current_branch': get_branch_info(repo_path)['current'],
            'total_branches': get_branch_info(repo_path)['total']
        },
        'contributors': get_contributors(repo_path, since_days)[:10],
        'commit_activity': {
            'by_day': get_commit_activity_by_day(repo_path, since_days or 30),
            'by_hour': get_commit_activity_by_hour(repo_path, since_days or 30)
        },
        'code_churn': get_code_churn(repo_path, since_days or 30),
        'most_changed_files': get_most_changed_files(repo_path, since_days or 30, 10),
        'branches': get_branch_info(repo_path),
        'last_commit': get_last_commit_info(repo_path)
    }
    
    if output_format == 'json':
        print(json.dumps(data, indent=2))
    else:
        print_text_report(data)

def print_text_report(data):
    """Print human-readable report"""
    print("=" * 60)
    print("📊 GIT REPOSITORY ANALYSIS")
    print("=" * 60)
    print(f"\n📁 Repository: {data['repository']}")
    print(f"📅 Period: {data['period_days']}")
    print(f"🕐 Analyzed: {data['analyzed_at'][:19]}")
    
    print("\n" + "─" * 60)
    print("📈 SUMMARY")
    print("─" * 60)
    s = data['summary']
    print(f"  Total Commits:     {s['total_commits']:,}")
    print(f"  Tracked Files:     {s['tracked_files']:,}")
    print(f"  Repository Size:   {s['repo_size']}")
    print(f"  Current Branch:    {s['current_branch']}")
    print(f"  Total Branches:    {s['total_branches']}")
    
    if data['last_commit']:
        print("\n" + "─" * 60)
        print("📝 LAST COMMIT")
        print("─" * 60)
        lc = data['last_commit']
        print(f"  Hash:    {lc['hash']}")
        print(f"  Author:  {lc['author']}")
        print(f"  Date:    {lc['date']}")
        print(f"  Message: {lc['message']}")
    
    if data['contributors']:
        print("\n" + "─" * 60)
        print("👥 TOP CONTRIBUTORS")
        print("─" * 60)
        for i, c in enumerate(data['contributors'][:5], 1):
            bar = "█" * int(c['commits'] / max(data['contributors'][0]['commits'], 1) * 20)
            print(f"  {i}. {c['name'][:25]:25} {c['commits']:4} {bar}")
    
    print("\n" + "─" * 60)
    print("📊 COMMIT ACTIVITY (by day)")
    print("─" * 60)
    days = data['commit_activity']['by_day']
    max_commits = max(days.values()) if days else 1
    for day, count in days.items():
        bar = "█" * int(count / max(max_commits, 1) * 30)
        print(f"  {day[:3]}: {count:3} {bar}")
    
    churn = data['code_churn']
    print("\n" + "─" * 60)
    print("🔄 CODE CHURN")
    print("─" * 60)
    print(f"  Insertions:   +{churn['insertions']:,}")
    print(f"  Deletions:    -{churn['deletions']:,}")
    print(f"  Net Change:   {churn['insertions'] - churn['deletions']:+,.0f}")
    print(f"  Files Touched: {churn['files_changed']:,}")
    
    if data['most_changed_files']:
        print("\n" + "─" * 60)
        print("📄 MOST CHANGED FILES")
        print("─" * 60)
        for f in data['most_changed_files'][:5]:
            print(f"  {f['changes']:3}x  {f['file'][:50]}")
    
    print("\n" + "=" * 60)
    print("Part of PD's Free Developer Tools")
    print("https://barrowryan89-cloud.github.io/pd-researcher/")
    print(f"\n💻 Level up your coding with JetBrains IDEs:")
    print("   https://www.jetbrains.com/?utm_source=pdresearcher [affiliate]")
    print("=" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze Git repository statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python git_analyzer_free.py                    # Analyze current directory
  python git_analyzer_free.py /path/to/repo      # Analyze specific repo
  python git_analyzer_free.py --days 7           # Last 7 days only
  python git_analyzer_free.py --format json      # JSON output
        """
    )
    
    parser.add_argument('path', nargs='?', default='.', help='Path to git repository (default: current directory)')
    parser.add_argument('--days', type=int, help='Only analyze last N days')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    # Expand path
    repo_path = os.path.expanduser(args.path)
    
    # Verify path exists
    if not os.path.isdir(repo_path):
        print(f"Error: Directory not found: {repo_path}")
        sys.exit(1)
    
    analyze_repo(repo_path, args.days, args.format)

if __name__ == '__main__':
    main()
