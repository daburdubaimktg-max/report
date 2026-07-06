# Copy-paste prompt for local Claude Code / Cowork

Open Claude Code (or Cowork) on your own computer, and paste the prompt below.
Replace `<PLAYLIST_URL>` with the real YouTube playlist URL of the 37-video
series (open your c.gle share link in a browser to find it).

---

Clone https://github.com/daburdubaimktg-max/report and check out the branch
`claude/rory-sutherland-transcripts-2ubc0p`. Then:

1. Install yt-dlp if missing (`pip install -U yt-dlp`).
2. Run: `bash scripts/fetch_transcripts.sh "<PLAYLIST_URL>"`
   — it downloads English captions for all videos in the playlist into
   `transcripts/raw/`. If any video has no captions at all, note it and
   continue; don't stop.
3. Run: `python3 scripts/clean_vtt.py transcripts/raw transcripts/clean`
4. Sanity-check: count the .txt files in `transcripts/clean/` (expect 37),
   and open two of them to confirm they read as clean prose with [mm:ss]
   timestamps, not raw caption markup.
5. Commit both `transcripts/raw/` and `transcripts/clean/` to the same branch
   with message "Add transcripts for 37-video Rory Sutherland series" and
   push to origin.
6. Report: how many transcripts succeeded, which videos (if any) had no
   captions, and the total word count.

---

Once the push is done, come back to the cloud session and say
"transcripts are pushed — run the analysis", and the deep per-video +
cross-corpus analysis will be run from `prompts/01` and `prompts/02`.
