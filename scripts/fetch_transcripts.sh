#!/usr/bin/env bash
# Batch-download subtitles for every video in a YouTube playlist/channel.
# Usage: bash scripts/fetch_transcripts.sh "<PLAYLIST_URL>"
set -euo pipefail

URL="${1:?Usage: fetch_transcripts.sh <playlist-or-channel-url>}"
OUT="transcripts/raw"
mkdir -p "$OUT"

# --write-subs        prefer manual (creator-uploaded) captions
# --write-auto-subs   fall back to YouTube's auto-generated captions
# --sub-langs         ONLY genuine English tracks. Do NOT use "en.*": that
#                     also matches en-fr, en-de, ... (auto-TRANSLATED tracks),
#                     which are useless here and trigger HTTP 429 rate limiting.
# --skip-download     captions only, no video files
yt-dlp \
  --skip-download \
  --write-subs \
  --write-auto-subs \
  --sub-langs "en,en-orig,en-US,en-GB,en-en" \
  --sub-format "vtt" \
  --sleep-requests 1 \
  --retries 10 \
  --extractor-retries 5 \
  -o "$OUT/%(playlist_index)02d - %(title)s.%(ext)s" \
  "$URL"

echo
echo "Done. Raw .vtt files in $OUT — now run:"
echo "  python3 scripts/clean_vtt.py $OUT transcripts/clean"
