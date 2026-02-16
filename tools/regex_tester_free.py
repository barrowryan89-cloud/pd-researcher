#!/usr/bin/env python3
"""
PD Regex Tester & Debugger - Tool #54
Test, debug, and explain regular expressions locally
SEO Keywords: regex tester, regex debugger, python regex, regex validator
"""

import re
import sys
import argparse
from typing import List, Dict, Optional, Tuple


class RegexTester:
    """Local regex testing and debugging tool"""
    
    # Common regex patterns for quick reference
    COMMON_PATTERNS = {
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "url": r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$",
        "ip": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        "phone": r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$",
        "hex": r"^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
        "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        "date": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$",
        "time": r"^([01]?\d|2[0-3]):[0-5]\d(:[0-5]\d)?$",
        "credit_card": r"^[0-9]{13,19}$",
        "password_strong": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    }
    
    FLAGS = {
        "i": re.IGNORECASE,
        "m": re.MULTILINE,
        "s": re.DOTALL,
        "x": re.VERBOSE,
        "a": re.ASCII,
        "l": re.LOCALE,
        "u": re.UNICODE,
    }
    
    def __init__(self, pattern: str, flags: str = ""):
        self.pattern = pattern
        self.flags = flags
        self.compiled = self._compile(pattern, flags)
        self.error = None
        
    def _compile(self, pattern: str, flags: str) -> Optional[re.Pattern]:
        """Compile regex with flags"""
        try:
            flag_val = 0
            for f in flags.lower():
                if f in self.FLAGS:
                    flag_val |= self.FLAGS[f]
            return re.compile(pattern, flag_val)
        except re.error as e:
            self.error = str(e)
            return None
    
    def test(self, text: str) -> Dict:
        """Test pattern against text"""
        if self.error:
            return {"error": self.error}
        
        result = {
            "matches": [],
            "groups": [],
            "match_count": 0,
            "is_match": False,
        }
        
        if not self.compiled:
            return result
        
        # Find all matches
        for match in self.compiled.finditer(text):
            result["is_match"] = True
            result["match_count"] += 1
            
            match_info = {
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
                "groups": [],
            }
            
            # Capture groups
            if match.groups():
                for i, group in enumerate(match.groups(), 1):
                    if group is not None:
                        match_info["groups"].append({
                            "num": i,
                            "text": group,
                            "start": match.start(i),
                            "end": match.end(i),
                        })
            
            result["matches"].append(match_info)
        
        # Also test full match
        full = self.compiled.match(text)
        result["full_match"] = bool(full)
        
        return result
    
    def explain(self) -> List[str]:
        """Provide human-readable explanation of pattern"""
        explanations = []
        pattern = self.pattern
        
        # Basic pattern components
        components = [
            (r"^", "Start of string"),
            (r"$", "End of string"),
            (r"\d", "Digit (0-9)"),
            (r"\D", "Non-digit"),
            (r"\w", "Word character (letter, digit, underscore)"),
            (r"\W", "Non-word character"),
            (r"\s", "Whitespace character"),
            (r"\S", "Non-whitespace character"),
            (r".", "Any character (except newline)"),
            (r"*", "Zero or more of preceding"),
            (r"+", "One or more of preceding"),
            (r"?", "Zero or one of preceding (optional)"),
            (r"{n}", "Exactly n of preceding"),
            (r"{n,}", "n or more of preceding"),
            (r"{n,m}", "Between n and m of preceding"),
            (r"[abc]", "Character class: any of a, b, or c"),
            (r"[^abc]", "Negated class: anything except a, b, c"),
            (r"|", "OR - alternation"),
            (r"()", "Capturing group"),
            (r"(?:)", "Non-capturing group"),
            (r"(?=)", "Positive lookahead"),
            (r"(?!)", "Negative lookahead"),
        ]
        
        for comp, desc in components:
            if comp in pattern:
                explanations.append(f"  {comp:12} → {desc}")
        
        return explanations if explanations else ["  (Pattern uses basic matching)"]
    
    def replace(self, text: str, replacement: str) -> str:
        """Perform substitution"""
        if self.error or not self.compiled:
            return text
        return self.compiled.sub(replacement, text)


def format_matches(result: Dict, text: str, colorize: bool = True) -> str:
    """Format match results with highlighting"""
    if "error" in result:
        return f"❌ ERROR: {result['error']}"
    
    lines = []
    
    if result["is_match"]:
        lines.append(f"✅ MATCH FOUND ({result['match_count']} occurrence(s))")
        lines.append("")
        
        # Show highlighted text
        if colorize:
            highlighted = text
            offset = 0
            for match in result["matches"]:
                start = match["start"] + offset
                end = match["end"] + offset
                hl = f"\033[1;32m{highlighted[start:end]}\033[0m"
                highlighted = highlighted[:start] + hl + highlighted[end:]
                offset += len(hl) - (end - start)
            lines.append(f"Text: {highlighted}")
        else:
            lines.append(f"Text: {text}")
        
        lines.append("")
        
        # Show match details
        for i, match in enumerate(result["matches"], 1):
            lines.append(f"  Match {i}:")
            lines.append(f"    Text:  '{match['text']}'")
            lines.append(f"    Range: [{match['start']}:{match['end']}]")
            
            if match["groups"]:
                lines.append(f"    Groups:")
                for g in match["groups"]:
                    lines.append(f"      {g['num']}: '{g['text']}' [{g['start']}:{g['end']}]")
            lines.append("")
        
        if result["full_match"]:
            lines.append("📍 Full string match: YES")
    else:
        lines.append("❌ No matches found")
        lines.append(f"   Text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="PD Regex Tester & Debugger - Test and debug regular expressions locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "\\d{3}-\\d{4}" "Call 555-1234 or 555-5678"
  %(prog)s -i "hello" "HELLO world"
  %(prog)s -r "\\d+" "XXX" "Room 101 and 202"
  %(prog)s -l                          # List common patterns
  %(prog)s -e "(?P<name>\\w+)"          # Explain pattern
        """
    )
    
    parser.add_argument("pattern", nargs="?", help="Regular expression pattern")
    parser.add_argument("text", nargs="?", help="Text to test against")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Case insensitive")
    parser.add_argument("-m", "--multiline", action="store_true", help="Multiline mode")
    parser.add_argument("-s", "--dotall", action="store_true", help="Dot matches newlines")
    parser.add_argument("-x", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-e", "--explain", action="store_true", help="Explain the pattern")
    parser.add_argument("-r", "--replace", metavar="REPL", help="Replace matches with REPL")
    parser.add_argument("-l", "--list", action="store_true", help="List common patterns")
    parser.add_argument("--no-color", action="store_true", help="Disable color output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode (exit code only)")
    
    args = parser.parse_args()
    
    # List common patterns
    if args.list:
        print("📚 Common Regex Patterns:")
        print("")
        for name, pattern in RegexTester.COMMON_PATTERNS.items():
            print(f"  {name:20} {pattern}")
        return 0
    
    # Validate args
    if not args.pattern:
        parser.print_help()
        return 1
    
    # Build flags string
    flags = ""
    if args.ignore_case:
        flags += "i"
    if args.multiline:
        flags += "m"
    if args.dotall:
        flags += "s"
    if args.verbose:
        flags += "x"
    
    # Create tester
    tester = RegexTester(args.pattern, flags)
    
    if tester.error:
        if not args.quiet:
            print(f"❌ Invalid regex: {tester.error}")
        return 2
    
    # Explain mode
    if args.explain:
        print(f"🔍 Pattern: /{args.pattern}/")
        if flags:
            print(f"   Flags:   {flags}")
        print("")
        print("Explanation:")
        for line in tester.explain():
            print(line)
        return 0
    
    # Need text for testing
    if args.text is None:
        # Try reading from stdin
        try:
            args.text = sys.stdin.read()
        except:
            parser.print_help()
            return 1
    
    # Replace mode
    if args.replace is not None:
        result = tester.replace(args.text, args.replace)
        print(result)
        return 0
    
    # Test mode
    result = tester.test(args.text)
    
    if args.quiet:
        return 0 if result.get("is_match") else 1
    
    # Print results
    print(f"🔍 Pattern: /{args.pattern}/")
    if flags:
        print(f"   Flags:   {flags}")
    print("")
    print(format_matches(result, args.text, colorize=not args.no_color))
    
    return 0 if result.get("is_match") else 1


if __name__ == "__main__":
    sys.exit(main())

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
