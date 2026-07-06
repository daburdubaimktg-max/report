#!/usr/bin/env bash
# Batch-download subtitles for every video in a YouTube playlist/channel.
# Usage: bash scripts/fetch_transcripts.sh "<PLAYLIST_URL>"
set -euo pipefail

URL="${1:?Usage: fetch_transcripts.sh <playlist-or-channel-url>}"
OUT="transcripts/raw"
mkdir -p "$OUT"

# --write-subs        prefer manual (creator-uploaded) captions
# --write-auto-subs   fall back to YouTube's auto-generated captions
# --sub-langs         all English variants (en, en-US, en-GB, en-orig)
# --skip-download     captions only, no video files
yt-dlp \
  --skip-download \
  --write-subs \
  --write-auto-subs \
  --sub-langs "en.*" \
  --sub-format "vtt" \
  --sleep-requests 1 \
  -o "$OUT/%(playlist_index)02d - %(title)s.%(ext)s" \
  "$URL"

echo
echo "Done. Raw .vtt files in $OUT — now run:"
echo "  python3 scripts/clean_vtt.py $OUT transcripts/clean"
