# 10links - High-Signal Search

Retrieve clean, distraction-free search results from [10links.blue](https://10links.blue). Perfect for agents who need raw URLs without the bloat of modern search engines.

## Tools

### `tenlinks_search`

Search the web and get a simple list of 10 relevant links.

**Parameters:**

- `query` (string, required): The search query.

**Usage:**

```json
{
  "query": "openclaw documentation"
}
```

## Implementation

```bash
#!/bin/bash

# Extract query from JSON input (stdin)
QUERY=$(jq -r '.query // empty')

if [ -z "$QUERY" ]; then
  echo '{"error": "Missing query parameter"}'
  exit 1
fi

# URL encode the query
ENCODED_QUERY=$(echo "$QUERY" | jq -sRr @uri | sed 's/%0A//g')

# Fetch results from 10links.blue
# Note: 10links.blue returns HTML. We use a simple grep/sed pipeline to extract links 
# for this MVP. A more robust implementation would use a proper HTML parser.
# This serves as a "high-signal" filter.

curl -s "https://10links.blue/search?q=$ENCODED_QUERY" | \
grep -oP 'href="\K[^"]+' | \
grep -vE '^\/|google|twitter|facebook|instagram|tiktok' | \
head -n 10 | \
jq -R . | jq -s '{links: .}'
```
