#!/bin/bash
# Convert markdown files to HTML and push to site

for f in content/*.md; do
    if [ -f "$f" ]; then
        basename=$(basename "$f" .md)
        # Simple markdown to HTML conversion
        {
            echo '<!DOCTYPE html><html><head><title>'$basename'</title></head><body>'
            echo '<article>'
            # Convert headers
            sed 's/^# \(.*\)/<h1>\1<\/h1>/g; s/^## \(.*\)/<h2>\1<\/h2>/g; s/^### \(.*\)/<h3>\1<\/h3>/g' "$f" | \
            sed 's/\*\*\(.*\)\*\*/<strong>\1<\/strong>/g' | \
            sed 's/\*\(.*\)\*/<em>\1<\/em>/g' | \
            sed 's/^- /<li>/g' | \
            sed 's/^$/<\/p><p>/g'
            echo '</article>'
            echo '</body></html>'
        } > "blog/${basename}.html"
        echo "Converted: $basename"
    fi
done

echo "Total converted: $(ls blog/*.html 2>/dev/null | wc -l)"
