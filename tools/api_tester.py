#!/usr/bin/env python3
"""
API Tester — Free Tool #31
Test any REST API endpoint with custom headers, methods, and payloads.
Part of the PD_Researcher free tools collection.
https://github.com/barrowryan89-cloud/pd-researcher
"""

import argparse
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode


def make_request(url, method="GET", headers=None, data=None, params=None):
    """Make HTTP request and return response details."""
    
    # Add query params if provided
    if params:
        url = f"{url}?{urlencode(params)}"
    
    # Prepare headers
    req_headers = {"User-Agent": "PD_Researcher-APITester/1.0"}
    if headers:
        req_headers.update(headers)
    
    # Prepare data
    req_data = None
    if data:
        if isinstance(data, dict):
            req_data = json.dumps(data).encode('utf-8')
            if 'Content-Type' not in req_headers:
                req_headers['Content-Type'] = 'application/json'
        else:
            req_data = data.encode('utf-8')
    
    try:
        req = Request(url, data=req_data, headers=req_headers, method=method.upper())
        
        with urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            response_headers = dict(response.headers)
            
            # Try to parse as JSON first
            try:
                body = json.loads(response.read().decode('utf-8'))
                body_formatted = json.dumps(body, indent=2)
                content_type = "json"
            except json.JSONDecodeError:
                body = response.read().decode('utf-8')
                body_formatted = body
                content_type = "text"
            
            return {
                "success": True,
                "status_code": status_code,
                "headers": response_headers,
                "body": body,
                "body_formatted": body_formatted,
                "content_type": content_type,
                "url": response.geturl()
            }
            
    except HTTPError as e:
        # HTTP errors (4xx, 5xx) still have response bodies
        try:
            error_body = e.read().decode('utf-8')
            try:
                error_body = json.loads(error_body)
                error_formatted = json.dumps(error_body, indent=2)
            except:
                error_formatted = error_body
        except:
            error_formatted = ""
        
        return {
            "success": False,
            "status_code": e.code,
            "headers": dict(e.headers) if e.headers else {},
            "body": error_body if error_body else None,
            "body_formatted": error_formatted,
            "error": f"HTTP Error {e.code}: {e.reason}",
            "url": e.url
        }
        
    except URLError as e:
        return {
            "success": False,
            "error": f"URL Error: {e.reason}",
            "url": url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "url": url
        }


def print_response(result, verbose=False):
    """Print formatted response."""
    
    # Status line with color hints
    if result["success"]:
        status_icon = "✓"
        status_line = f"{status_icon} Status: {result['status_code']}"
    else:
        if "status_code" in result:
            status_icon = "✗"
            status_line = f"{status_icon} Status: {result['status_code']}"
        else:
            status_icon = "✗"
            status_line = f"{status_icon} Error: {result.get('error', 'Unknown error')}"
    
    print(f"\n{'='*60}")
    print(f"{status_line}")
    print(f"URL: {result.get('url', 'N/A')}")
    print(f"{'='*60}")
    
    if verbose and "headers" in result:
        print("\n📋 Response Headers:")
        for key, value in result["headers"].items():
            print(f"  {key}: {value}")
    
    if "body_formatted" in result and result["body_formatted"]:
        print(f"\n📦 Response Body:")
        print(result["body_formatted"])
    
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="API Tester — Test any REST API endpoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple GET request
  python api_tester.py https://api.github.com/users/octocat
  
  # POST with JSON data
  python api_tester.py https://httpbin.org/post -m POST -d '{"key": "value"}'
  
  # With custom headers
  python api_tester.py https://api.example.com/data -H "Authorization: Bearer token123"
  
  # With query parameters
  python api_tester.py https://api.example.com/search -q "q=python&limit=10"
  
  # Verbose output (shows all headers)
  python api_tester.py https://api.github.com -v
        """
    )
    
    parser.add_argument("url", help="API endpoint URL")
    parser.add_argument("-m", "--method", default="GET",
                       choices=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
                       help="HTTP method (default: GET)")
    parser.add_argument("-H", "--header", action="append",
                       help="Custom header (format: 'Key: Value'). Can be used multiple times.")
    parser.add_argument("-d", "--data",
                       help="Request body data (JSON string or raw text)")
    parser.add_argument("-q", "--query",
                       help="Query parameters (format: 'key1=value1&key2=value2')")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output (show all headers)")
    parser.add_argument("--json", action="store_true",
                       help="Output raw JSON (for piping)")
    
    args = parser.parse_args()
    
    # Parse headers
    headers = {}
    if args.header:
        for header in args.header:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
            else:
                print(f"⚠️  Warning: Invalid header format: {header}")
    
    # Parse query params
    params = {}
    if args.query:
        for param in args.query.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                params[key] = value
    
    # Parse data - try JSON first
    data = args.data
    if data:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass  # Keep as string
    
    # Make request
    result = make_request(args.url, args.method, headers, data, params if params else None)
    
    # Output
    if args.json:
        # Remove formatted body for JSON output
        output = {k: v for k, v in result.items() if k != "body_formatted"}
        print(json.dumps(output, indent=2, default=str))
    else:
        print_response(result, args.verbose)
    
    # Exit with error code on failure
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
