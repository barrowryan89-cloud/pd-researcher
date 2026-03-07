#!/usr/bin/env python3
"""
Tool #34: HTML Table Generator
Convert CSV data to HTML tables with styling options
"""

import sys
import csv
import html


def csv_to_html_table(csv_file, title="", striped=True, bordered=True):
    """Convert CSV to styled HTML table."""
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        return None, str(e)
    
    if not rows:
        return None, "CSV file is empty"
    
    # Build HTML
    html_parts = ['<table>']
    
    # Header row
    html_parts.append('  <thead>')
    html_parts.append('    <tr>')
    for cell in rows[0]:
        html_parts.append(f'      <th>{html.escape(cell)}</th>')
    html_parts.append('    </tr>')
    html_parts.append('  </thead>')
    
    # Body rows
    if len(rows) > 1:
        html_parts.append('  <tbody>')
        for i, row in enumerate(rows[1:], 1):
            row_class = ' class="striped"' if striped and i % 2 == 0 else ''
            html_parts.append(f'    <tr{row_class}>')
            for cell in row:
                html_parts.append(f'      <td>{html.escape(cell)}</td>')
            html_parts.append('    </tr>')
        html_parts.append('  </tbody>')
    
    html_parts.append('</table>')
    
    table_html = '\n'.join(html_parts)
    
    # Wrap in full HTML document
    border_style = 'border: 1px solid #ddd;' if bordered else ''
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html.escape(title) or 'CSV Table'}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 40px; }}
        table {{ {border_style} border-collapse: collapse; width: 100%; max-width: 100%; }}
        th, td {{ padding: 12px; text-align: left; {border_style} }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        tr:hover {{ background: #f8f9fa; }}
        .striped {{ background: #fafafa; }}
    </style>
</head>
<body>
    <h1>{html.escape(title) or 'Data Table'}</h1>
    {table_html}
</body>
</html>"""
    
    return full_html, None


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 html_table_generator_free.py <input.csv> [output.html] [title]")
        print("Example: python3 html_table_generator_free.py data.csv report.html 'Sales Report'")
        print("\nOptions:")
        print("  --no-striped    Disable alternating row colors")
        print("  --no-border     Disable table borders")
        sys.exit(0)
    
    args = sys.argv[1:]
    
    striped = '--no-striped' not in args
    bordered = '--no-border' not in args
    
    # Remove flags from args
    args = [a for a in args if not a.startswith('--')]
    
    if not args:
        print("Error: No input file specified")
        sys.exit(1)
    
    input_file = args[0]
    output_file = args[1] if len(args) > 1 else input_file.replace('.csv', '.html')
    title = args[2] if len(args) > 2 else ""
    
    html_output, error = csv_to_html_table(input_file, title, striped, bordered)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"✓ Created: {output_file}")
        print(f"  Source: {input_file}")
        print(f"  Title: {title or 'Data Table'}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
