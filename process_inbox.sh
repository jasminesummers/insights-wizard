#!/bin/bash
# ==============================================================================
#  process_inbox.sh — Mass Batch Ingestion script for Transcripts & PDFs
# ==============================================================================
#  Drop any PDF, .txt, or .md interview transcript files into:
#    slides_updater/inbox/
#
#  Then run:
#    ./process_inbox.sh
# ==============================================================================

PROJECT_DIR="/usr/local/google/home/jasminesummers/Documents/Insights Wizard"
INBOX_DIR="$PROJECT_DIR/inbox"
PROCESSED_DIR="$INBOX_DIR/processed"

cd "$PROJECT_DIR" || exit 1

echo "🔍 Scanning inbox folder ($INBOX_DIR) for new transcript files..."

COUNT=0
for FILE in "$INBOX_DIR"/*; do
  if [ -f "$FILE" ]; then
    BASENAME=$(basename "$FILE")
    echo "📄 Found new document: $BASENAME"
    
    # If PDF, convert text extract using pdftotext
    if [[ "$BASENAME" == *.pdf ]]; then
      TXT_FILE="$INBOX_DIR/${BASENAME%.pdf}.txt"
      pdftotext "$FILE" "$TXT_FILE"
      echo "   └─ Converted PDF to text: $(basename "$TXT_FILE")"
    fi
    
    COUNT=$((COUNT + 1))
  fi
done

if [ "$COUNT" -eq 0 ]; then
  echo "✨ No unanalyzed files in inbox/! Drop transcripts there anytime."
  exit 0
fi

echo "=========================================================="
echo "🎉 Found $COUNT file(s) ready for quote extraction!"
echo "👉 Tell Jetski in chat: 'Process the transcripts in my inbox'"
echo "   and all quotes will be categorized into your slide deck!"
echo "=========================================================="
