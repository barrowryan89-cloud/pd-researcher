#!/usr/bin/env python3
"""
DiffText - Free CLI Tool #42
Compare two texts or files and show differences
Zero dependencies, single file, MIT licensed
https://github.com/barrowryan89-cloud/pd-researcher
"""

import sys
import argparse
import difflib

__version__ = "1.0.0"

def read_input(source):
    """Read text from file or return string."""
    if source == '-':
        return sys.stdin.read()
    try:
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return source  # Treat as literal string
    except Exception as e:
        print(f"❌ Error reading {source}: {e}", file=sys.stderr)
        sys.exit(1)

def unified_diff(text1, text2, label1='original', label2='modified', context=3):
    """Generate unified diff."""
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    
    if not lines1:
        lines1 = ['']
    if not lines2:
        lines2 = ['']
    
    diff = difflib.unified_diff(
        lines1, lines2,
        fromfile=label1, tofile=label2,
        lineterm='',
        n=context
    )
    return '\n'.join(diff)

def side_by_side_diff(text1, text2, width=40):
    """Generate side-by-side comparison."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    max_len = max(len(lines1), len(lines2))
    lines1.extend([''] * (max_len - len(lines1)))
    lines2.extend([''] * (max_len - len(lines2)))
    
    output = []
    output.append(f"{'ORIGINAL':{width}} │ {'MODIFIED':{width}}")
    output.append('─' * width + '─┼─' + '─' * width)
    
    for i, (l1, l2) in enumerate(zip(lines1, lines2)):
        l1_display = l1[:width-1] if len(l1) > width else l1
        l2_display = l2[:width-1] if len(l2) > width else l2
        
        if l1 != l2:
            marker = '≠'
        else:
            marker = '│'
        
        output.append(f"{l1_display:{width}} {marker} {l2_display:{width}}")
    
    return '\n'.join(output)

def simple_diff(text1, text2):
    """Generate simple line-by-line diff."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    output = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for line in lines1[i1:i2]:
                output.append(f"  {line}")
        elif tag == 'delete':
            for line in lines1[i1:i2]:
                output.append(f"- {line}")
        elif tag == 'insert':
            for line in lines2[j1:j2]:
                output.append(f"+ {line}")
        elif tag == 'replace':
            for line in lines1[i1:i2]:
                output.append(f"- {line}")
            for line in lines2[j1:j2]:
                output.append(f"+ {line}")
    
    return '\n'.join(output)

def word_diff(text1, text2):
    """Generate word-level diff."""
    words1 = text1.split()
    words2 = text2.split()
    
    matcher = difflib.SequenceMatcher(None, words1, words2)
    output = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            output.append(' '.join(words1[i1:i2]))
        elif tag == 'delete':
            deleted = ' '.join(words1[i1:i2])
            output.append(f"[-{deleted}-]")
        elif tag == 'insert':
            inserted = ' '.join(words2[j1:j2])
            output.append(f"{{+{inserted}+}}")
        elif tag == 'replace':
            deleted = ' '.join(words1[i1:i2])
            inserted = ' '.join(words2[j1:j2])
            output.append(f"[-{deleted}-]{{+{inserted}+}}")
    
    return ' '.join(output)

def stats(text1, text2):
    """Calculate diff statistics."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    
    added = 0
    removed = 0
    changed = 0
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'insert':
            added += j2 - j1
        elif tag == 'delete':
            removed += i2 - i1
        elif tag == 'replace':
            changed += max(i2 - i1, j2 - j1)
    
    similarity = matcher.ratio()
    
    return {
        'lines_original': len(lines1),
        'lines_modified': len(lines2),
        'lines_added': added,
        'lines_removed': removed,
        'lines_changed': changed,
        'similarity': similarity
    }

def main():
    parser = argparse.ArgumentParser(
        description="📝 DiffText - Compare two texts or files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file1.txt file2.txt              # Compare files
  %(prog)s -s "hello" "world"               # Compare strings
  %(prog)s -u file1.txt file2.txt           # Unified diff
  %(prog)s --side-by-side a.txt b.txt       # Side by side
  cat file1.txt | %(prog)s - file2.txt      # Stdin vs file

Modes:
  simple        Line additions/deletions (default)
  unified       Standard unified diff format
  side-by-side  Two column comparison
  word          Word-level changes
        """
    )
    parser.add_argument('source1', help='First file or "-" for stdin')
    parser.add_argument('source2', help='Second file or text string')
    parser.add_argument('-s', '--strings', action='store_true',
                       help='Treat arguments as literal strings, not files')
    parser.add_argument('-m', '--mode', default='simple',
                       choices=['simple', 'unified', 'side-by-side', 'word'],
                       help='Diff mode (default: simple)')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics only')
    parser.add_argument('-c', '--context', type=int, default=3,
                       help='Context lines for unified diff (default: 3)')
    parser.add_argument('-w', '--width', type=int, default=40,
                       help='Column width for side-by-side (default: 40)')
    parser.add_argument('-v', '--version', action='version',
                       version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    if args.strings:
        text1 = args.source1
        text2 = args.source2
    else:
        text1 = read_input(args.source1)
        text2 = read_input(args.source2)
    
    if args.stats:
        s = stats(text1, text2)
        print("═" * 50)
        print("📊 Diff Statistics")
        print("═" * 50)
        print(f"  Original lines:   {s['lines_original']}")
        print(f"  Modified lines:   {s['lines_modified']}")
        print(f"  Lines added:      {s['lines_added']}")
        print(f"  Lines removed:    {s['lines_removed']}")
        print(f"  Lines changed:    {s['lines_changed']}")
        print(f"  Similarity:       {s['similarity']:.1%}")
        print("═" * 50)
        return
    
    print("═" * 60)
    print("📝 DiffText - Text Comparison Tool")
    print("═" * 60)
    
    print(f"\n📄 Mode: {args.mode}")
    print(f"📊 Source 1: {len(text1)} chars, {len(text1.splitlines())} lines")
    print(f"📊 Source 2: {len(text2)} chars, {len(text2.splitlines())} lines")
    print()
    
    if args.mode == 'simple':
        result = simple_diff(text1, text2)
    elif args.mode == 'unified':
        result = unified_diff(text1, text2, args.source1, args.source2, args.context)
    elif args.mode == 'side-by-side':
        result = side_by_side_diff(text1, text2, args.width)
    elif args.mode == 'word':
        result = word_diff(text1, text2)
    
    if result.strip():
        print(result)
    else:
        print("✅ Texts are identical")
    
    s = stats(text1, text2)
    print(f"\n📈 Similarity: {s['similarity']:.1%}")
    
    print("═" * 60)
    print("\n💡 Pro Tip: Need directory comparison, patching, or 3-way merge?")
    print("   Check out PD_Researcher Pro → https://10links.blue")
    print("═" * 60)

if __name__ == '__main__':
    main()
