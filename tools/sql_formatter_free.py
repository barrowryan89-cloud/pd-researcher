#!/usr/bin/env python3
"""
PD SQL Formatter & Beautifier (Tool #56)
Free CLI tool for formatting and minifying SQL queries
Zero dependencies, single-file script
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional


class SQLFormatter:
    """SQL formatter with beautify and minify capabilities"""
    
    # SQL keywords that should be on their own line (uppercase)
    KEYWORDS = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'INSERT', 'UPDATE', 'DELETE',
        'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'ON', 'GROUP', 'BY',
        'ORDER', 'HAVING', 'LIMIT', 'OFFSET', 'UNION', 'ALL', 'VALUES',
        'SET', 'CREATE', 'TABLE', 'ALTER', 'DROP', 'INDEX', 'VIEW',
        'DISTINCT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'AS', 'IN',
        'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL', 'NOT', 'PRIMARY', 'KEY',
        'FOREIGN', 'REFERENCES', 'DEFAULT', 'AUTO_INCREMENT', 'UNIQUE'
    ]
    
    # Keywords that start new sections
    SECTION_KEYWORDS = ['SELECT', 'FROM', 'WHERE', 'GROUP', 'ORDER', 'HAVING', 'LIMIT', 'UNION']
    
    def __init__(self, indent_size: int = 4, uppercase_keywords: bool = True):
        self.indent_size = indent_size
        self.uppercase_keywords = uppercase_keywords
        self.keyword_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(kw) for kw in self.KEYWORDS) + r')\b',
            re.IGNORECASE
        )
    
    def _tokenize(self, sql: str) -> List[str]:
        """Tokenize SQL into manageable pieces"""
        # Normalize whitespace
        sql = ' '.join(sql.split())
        
        # Split on special characters while keeping them
        tokens = []
        current = ''
        for char in sql:
            if char in '(),;':
                if current.strip():
                    tokens.append(current.strip())
                tokens.append(char)
                current = ''
            else:
                current += char
        if current.strip():
            tokens.append(current.strip())
        
        return tokens
    
    def beautify(self, sql: str) -> str:
        """Format SQL with proper indentation"""
        if not sql.strip():
            return ''
        
        # Normalize and tokenize
        sql = sql.strip()
        tokens = self._tokenize(sql)
        
        result = []
        indent_level = 0
        in_select_list = False
        parens_depth = 0
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            upper_token = token.upper()
            
            # Handle parentheses
            if token == '(':
                parens_depth += 1
                if i > 0 and tokens[i-1].upper() in ('VALUES', 'IN'):
                    result.append(' ')
                result.append(token)
                if i + 1 < len(tokens) and tokens[i+1] != ')':
                    indent_level += 1
                    result.append('\n' + ' ' * self.indent_size * indent_level)
                i += 1
                continue
            
            if token == ')':
                if parens_depth > 0:
                    parens_depth -= 1
                if indent_level > 0:
                    indent_level -= 1
                # Remove trailing newline before closing paren
                if result and result[-1].endswith(' ' * self.indent_size * (indent_level + 1)):
                    result[-1] = result[-1].rstrip()
                result.append('\n' + ' ' * self.indent_size * indent_level + token)
                i += 1
                continue
            
            # Handle semicolons
            if token == ';':
                result.append(token)
                if i + 1 < len(tokens):
                    result.append('\n\n')
                i += 1
                continue
            
            # Handle commas (in SELECT list)
            if token == ',':
                result.append(token)
                if in_select_list:
                    result.append('\n' + ' ' * self.indent_size * indent_level + '    ')
                else:
                    result.append(' ')
                i += 1
                continue
            
            # Handle keywords
            if upper_token in self.KEYWORDS:
                # Handle section-starting keywords
                if upper_token in self.SECTION_KEYWORDS:
                    if result:
                        result.append('\n')
                    indent_level = 0
                    in_select_list = (upper_token == 'SELECT')
                    
                    if self.uppercase_keywords:
                        token = token.upper()
                    result.append(' ' * self.indent_size * indent_level + token)
                    
                    # Add newline after SELECT columns start
                    if upper_token == 'SELECT':
                        result.append('\n' + ' ' * self.indent_size + '    ')
                    else:
                        result.append(' ')
                
                elif upper_token in ('AND', 'OR'):
                    if result:
                        result.append('\n' + ' ' * self.indent_size * (indent_level + 1))
                    if self.uppercase_keywords:
                        token = token.upper()
                    result.append(token + ' ')
                
                else:
                    if self.uppercase_keywords:
                        token = token.upper()
                    result.append(token + ' ')
            
            else:
                # Regular token
                result.append(token)
                if i + 1 < len(tokens) and tokens[i + 1] not in (',', ')', ';'):
                    result.append(' ')
            
            i += 1
        
        formatted = ''.join(result).strip()
        
        # Clean up multiple newlines
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        
        return formatted
    
    def minify(self, sql: str) -> str:
        """Minify SQL by removing whitespace and comments"""
        if not sql.strip():
            return ''
        
        # Remove single-line comments
        sql = re.sub(r'--[^\n]*', '', sql)
        
        # Remove multi-line comments
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        
        # Normalize whitespace
        sql = ' '.join(sql.split())
        
        # Preserve space after keywords that need it
        sql = re.sub(r'\b(SELECT|FROM|WHERE|AND|OR|SET|VALUES)\s*', r'\1 ', sql, flags=re.IGNORECASE)
        
        return sql.strip()
    
    def validate(self, sql: str) -> dict:
        """Basic SQL validation - check for common issues"""
        issues = []
        upper_sql = sql.upper()
        
        # Check for unclosed parentheses
        open_parens = sql.count('(')
        close_parens = sql.count(')')
        if open_parens != close_parens:
            issues.append(f"Unclosed parentheses: {open_parens} open, {close_parens} close")
        
        # Check for unclosed quotes
        single_quotes = sql.count("'") - sql.count("\\'")
        if single_quotes % 2 != 0:
            issues.append("Unclosed single quotes")
        
        double_quotes = sql.count('"') - sql.count('\\"')
        if double_quotes % 2 != 0:
            issues.append("Unclosed double quotes")
        
        # Check for missing WHERE in DELETE/UPDATE
        if upper_sql.startswith('DELETE') and 'WHERE' not in upper_sql:
            issues.append("DELETE without WHERE clause (will delete all rows)")
        
        if upper_sql.startswith('UPDATE') and 'WHERE' not in upper_sql:
            issues.append("UPDATE without WHERE clause (will update all rows)")
        
        # Check for SELECT *
        if re.search(r'SELECT\s+\*', sql, re.IGNORECASE) and 'COUNT(' not in upper_sql:
            issues.append("Using SELECT * (consider specifying columns)")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': len(issues)
        }
    
    def analyze(self, sql: str) -> dict:
        """Analyze SQL query statistics"""
        upper_sql = sql.upper()
        
        return {
            'query_type': self._detect_query_type(upper_sql),
            'tables': len(re.findall(r'\bFROM\s+(\w+)|\bJOIN\s+(\w+)', sql, re.IGNORECASE)),
            'columns': len(re.findall(r'\bSELECT\s+(.+?)\s+FROM', sql, re.IGNORECASE)),
            'joins': len(re.findall(r'\bJOIN\b', upper_sql)),
            'conditions': len(re.findall(r'\bWHERE\b|\bAND\b|\bOR\b', upper_sql)),
            'subqueries': sql.count('('),
            'length_chars': len(sql),
            'length_lines': sql.count('\n') + 1
        }
    
    def _detect_query_type(self, upper_sql: str) -> str:
        """Detect the type of SQL query"""
        if upper_sql.startswith('SELECT'):
            return 'SELECT'
        elif upper_sql.startswith('INSERT'):
            return 'INSERT'
        elif upper_sql.startswith('UPDATE'):
            return 'UPDATE'
        elif upper_sql.startswith('DELETE'):
            return 'DELETE'
        elif upper_sql.startswith('CREATE'):
            return 'CREATE'
        elif upper_sql.startswith('ALTER'):
            return 'ALTER'
        elif upper_sql.startswith('DROP'):
            return 'DROP'
        else:
            return 'OTHER'


def main():
    parser = argparse.ArgumentParser(
        description='SQL Formatter & Beautifier - Free CLI Tool by PD',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i query.sql -o formatted.sql         # Format a file
  %(prog)s --minify -i query.sql                 # Minify SQL
  %(prog)s --validate query.sql                  # Validate SQL
  %(prog)s --analyze query.sql                   # Analyze SQL stats
  cat query.sql | %(prog)s                       # Read from stdin
  echo "SELECT * FROM users" | %(prog)s          # Format inline
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input SQL file (default: stdin)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-i', '--in-place', action='store_true',
                       help='Edit file in place (creates .bak backup)')
    parser.add_argument('--minify', action='store_true',
                       help='Minify instead of beautify')
    parser.add_argument('--validate', action='store_true',
                       help='Validate SQL for common issues')
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze SQL and show statistics')
    parser.add_argument('--indent', type=int, default=4,
                       help='Indentation size (default: 4)')
    parser.add_argument('--no-uppercase', action='store_true',
                       help='Do not uppercase SQL keywords')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        try:
            sql = Path(args.input).read_text()
        except FileNotFoundError:
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        sql = sys.stdin.read()
    
    if not sql.strip():
        print("Error: No SQL input provided", file=sys.stderr)
        sys.exit(1)
    
    # Create formatter
    formatter = SQLFormatter(
        indent_size=args.indent,
        uppercase_keywords=not args.no_uppercase
    )
    
    # Process based on mode
    if args.validate:
        result = formatter.validate(sql)
        print(f"Validation: {'✓ PASSED' if result['valid'] else '✗ ISSUES FOUND'}")
        if result['issues']:
            for issue in result['issues']:
                print(f"  - {issue}")
    
    elif args.analyze:
        stats = formatter.analyze(sql)
        print("SQL Analysis:")
        print(f"  Query Type: {stats['query_type']}")
        print(f"  Tables Referenced: {stats['tables']}")
        print(f"  Joins: {stats['joins']}")
        print(f"  Conditions: {stats['conditions']}")
        print(f"  Subqueries/Parens: {stats['subqueries']}")
        print(f"  Length: {stats['length_chars']} chars, {stats['length_lines']} lines")
    
    else:
        # Format or minify
        if args.minify:
            output = formatter.minify(sql)
        else:
            output = formatter.beautify(sql)
        
        # Output result
        if args.in_place and args.input:
            # Create backup
            backup_path = str(args.input) + '.bak'
            Path(args.input).rename(backup_path)
            Path(args.input).write_text(output)
            print(f"Formatted: {args.input} (backup: {backup_path})")
        elif args.output:
            Path(args.output).write_text(output)
            print(f"Formatted SQL written to: {args.output}")
        else:
            print(output)


if __name__ == '__main__':
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
