#!/usr/bin/env bash
set -euo pipefail

ACCOUNT="barrowryan89@gmail.com"
BACKUP_PARENT_ID="18UcdeWwnwkMSrEBjMzCaY-0-SxRRBtl2"

TS_UTC=$(date -u +"%Y-%m-%dT%H%MZ")
TODAY=$(date -u +"%F")

# Create a timestamped subfolder for this run
RUN_NAME="backup_${TS_UTC}"
RUN_ID=$(gog drive mkdir "$RUN_NAME" --account "$ACCOUNT" --parent "$BACKUP_PARENT_ID" --plain | awk -F'\t' '/^id\t/{print $2}')

log(){ echo "$*"; }

log "Backup folder: $RUN_NAME ($RUN_ID)"

# Core continuity files
for f in "MEMORY.md" "memory/${TODAY}.md"; do
  if [[ -f "$f" ]]; then
    gog drive upload "$f" --account "$ACCOUNT" --parent "$RUN_ID" --plain >/dev/null
    log "Uploaded: $f"
  fi
done

# Key product artifacts (keep small + practical)
shopt -s nullglob
for f in products/*.txt products/*_thread.txt products/*_draft.txt products/*_status.txt products/*.zip; do
  # Ryan directive: do not touch 10links artifacts
  if [[ "$f" == products/10links* ]]; then
    continue
  fi
  if [[ -f "$f" ]]; then
    gog drive upload "$f" --account "$ACCOUNT" --parent "$RUN_ID" --plain >/dev/null
    log "Uploaded: $f"
  fi
done

# Write a manifest locally and upload it too
MANIFEST="/tmp/${RUN_NAME}_manifest.txt"
{
  echo "Backup manifest: ${RUN_NAME}"
  echo "UTC: ${TS_UTC}"
  echo ""
  echo "Files included:"
  echo "- MEMORY.md (if present)"
  echo "- memory/${TODAY}.md (if present)"
  echo "- products/*.txt, *_thread.txt, *_draft.txt, *_status.txt, *.zip (if present)" 
  echo "- EXCLUDING: products/10links*"
} > "$MANIFEST"

gog drive upload "$MANIFEST" --name "manifest.txt" --account "$ACCOUNT" --parent "$RUN_ID" --plain >/dev/null
log "Uploaded: manifest.txt"

# Print folder link
FOLDER_URL=$(gog drive url "$RUN_ID" --account "$ACCOUNT" --plain | awk -F'\t' '{print $2}' | tail -n 1)
log "Drive folder: $FOLDER_URL"
