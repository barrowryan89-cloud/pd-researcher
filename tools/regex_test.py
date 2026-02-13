#!/usr/bin/env python3
"""
regex_test - Regular expression tester
Part of PD Researcher Tool Suite
"""

import sys
import re
import argparse

def test_regex(pattern, text, flags=0):
    """Test regex pattern against text."""
    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        return {'error': f"Invalid regex: {e}"}
    
    matches = list(compiled.finditer(text))
    
    return {
        'pattern': pattern,
        'flags': flags,
        'match_count': len(matches),
        'matches': [
            {
                'text': m.group(),
                'start': m.start(),
                'end': m.end(),
                'groups': m.groups(),
                'groupdict': m.groupdict()
            }
            for m in matches
        ],
        'groups': compiled.groups,
        'groupindex': dict(compiled.groupindex)
    }

def explain_regex(pattern):
    """Provide a basic explanation of regex components."""
    explanations = {
        '.': 'Any character except newline',
        '^': 'Start of string',
        '$': 'End of string',
        '*': 'Zero or more of preceding',
        '+': 'One or more of preceding',
        '?': 'Zero or one of preceding',
        '{': 'Quantifier start',
        '}': 'Quantifier end',
        '[': 'Character class start',
        ']': 'Character class end',
        '\\d': 'Digit [0-9]',
        '\\w': 'Word character [a-zA-Z0-9_]',
        '\\s': 'Whitespace',
        '\\b': 'Word boundary',
        '|': 'Alternation (OR)',
        '(': 'Group start',
        ')': 'Group end',
        '(?:': 'Non-capturing group',
        '(?P<': 'Named group',
        '(?=': 'Positive lookahead',
        '(?!': 'Negative lookahead',
    }
    
    found = []
    for key, desc in explanations.items():
        if key in pattern:
            found.append(f"  {key:8} → {desc}")
    
    return found

def main():
    parser = argparse.ArgumentParser(
        description='Regular expression tester',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "\\d+" "abc123def456"
  %(prog)s -i "hello" "HELLO world"      # case insensitive
  %(prog)s -m "^(\\w+)@(\\w+)" "test@email.com"
  echo "test string" | %(prog)s "\\w+"     # from stdin

Flags:
  -i  IGNORECASE  -m  MULTILINE
  -s  DOTALL      -v  VERBOSE
        """
    )
    parser.add_argument('pattern', help='Regular expression pattern')
    parser.add_argument('text', nargs='?', help='Text to match (or use stdin)')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Case insensitive')
    parser.add_argument('-m', '--multiline', action='store_true', help='Multiline mode')
    parser.add_argument('-s', '--dotall', action='store_true', help='Dot matches newlines')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose regex')
    parser.add_argument('-e', '--explain', action='store_true', help='Explain pattern')
    parser.add_argument('-r', '--replace', help='Replace matches with this string')
    parser.add_argument('-l', '--list', action='store_true', help='List only matches (one per line)')
    
    args = parser.parse_args()
    
    # Build flags
    flags = 0
    if args.ignore_case:
        flags |= re.IGNORECASE
    if args.multiline:
        flags |= re.MULTILINE
    if args.dotall:
        flags |= re.DOTALL
    if args.verbose:
        flags |= re.VERBOSE
    
    # Read text
    if args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)
    
    # Explain mode
    if args.explain:
        print(f"Pattern: {args.pattern}")
        explanations = explain_regex(args.pattern)
        if explanations:
            print("\nComponents found:")
            print('\n'.join(explanations))
        else:
            print("\nNo common components recognized")
        sys.exit(0)
    
    # Replace mode
    if args.replace is not None:
        try:
            result = re.sub(args.pattern, args.replace, text, flags=flags)
            print(result)
            sys.exit(0)
        except re.error as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Test mode
    result = test_regex(args.pattern, text, flags)
    
    if 'error' in result:
        print(result['error'], file=sys.stderr)
        sys.exit(1)
    
    if args.list:
        for match in result['matches']:
            print(match['text'])
        sys.exit(0)
    
    # Display results
    flag_names = []
    if flags & re.IGNORECASE: flag_names.append('IGNORECASE')
    if flags & re.MULTILINE: flag_names.append('MULTILINE')
    if flags & re.DOTALL: flag_names.append('DOTALL')
    if flags & re.VERBOSE: flag_names.append('VERBOSE')
    
    print(f"Pattern: {result['pattern']}")
    print(f"Flags:   {', '.join(flag_names) or 'none'}")
    print(f"Groups:  {result['groups']}")
    print(f"Matches: {result['match_count']}")
    
    if result['matches']:
        print("\nMatch details:")
        for i, match in enumerate(result['matches'], 1):
            print(f"\n  Match {i}:")
            print(f"    Text:  \"{match['text']}\"")
            print(f"    Pos:   {match['start']}-{match['end']}")
            if match['groups']:
                print(f"    Groups: {match['groups']}")
            if match['groupdict']:
                print(f"    Named:  {match['groupdict']}")
    else:
        print("\nNo matches found")

if __name__ == '__main__':
    main()
