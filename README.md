# Rory Sutherland — "Psychology of Irrational Value" Transcript & Analysis

Accurate, usable transcripts and a **deep (non-superficial) analysis** of the
Rory Sutherland "irrational value" corpus, plus the reusable pipeline that
produced them.

## What's in this repo (complete — all 37 videos)

- **`transcripts/clean/`** — 37 accurate, timestamped transcripts (~381,000
  words), cleaned from YouTube captions. Covers the full *Alchemy* talk,
  TEDxOxford / TEDxBrighton / TEDxNewSt, the Nudgestock keynotes, the 2-hour
  long-form interviews (Diary of a CEO, Modern Wisdom), the Scott Galloway
  brand debate, and the Georgist / culture-war material.
- **`transcripts/analysis/01.md … 37.md`** — a deep 9-section analysis of each
  video (thesis, argument chain, named principles traced to their originating
  researchers, every case study rated load-bearing vs. rhetorical, quotable
  lines with timestamps, contrarian claims with steelmen, applications,
  critical evaluation). Each was produced by a model reading the *entire*
  transcript — the depth NotebookLM's snippet-retrieval can't reach.
- **`SYNTHESIS.md`** — the capstone across all 37: Sutherland's unified theory
  of value, ~18 ranked recurring principles, a taxonomy of irrational value,
  his intellectual toolkit, cross-video contradictions, the repeatable
  "Sutherland Method," a ~20-tactic playbook, a thematic study guide, the 20
  best verbatim quotes, and open questions — all cited back to video numbers.
- **`transcripts/SOURCES.md`** — video-ID provenance for all 37.

Shareable zips are regenerated into `dist/` (gitignored): a transcripts
archive, an analyses archive, and a combined full-report archive.

> **Note:** video #18 ("Sweat the Small Stuff") is the same talk first used to
> demo the pipeline in `demo/` — one genuine duplicate in the source list.

---

## The reusable pipeline

## Why NotebookLM failed you

Two structural reasons, not a settings problem:

1. **NotebookLM never exposes verbatim transcripts.** It ingests the YouTube
   transcript internally as a source, but the product only lets you chat over
   it — there is no "export transcript" path.
2. **Its analysis is retrieval-based (RAG).** For any question it pulls a
   handful of short snippets from across your 37 sources and answers from
   those. It never reads any video end-to-end, which is exactly why the
   analysis feels superficial. Deep analysis requires putting each *full*
   transcript into a model's context window — that's the workflow below.

## The pipeline (best → fallback)

### Step 1 — Get the transcripts with `yt-dlp` (10 minutes, free, batch)

YouTube already has captions for every video; `yt-dlp` downloads all 37 in one
command. This is the most efficient method by a wide margin.

```bash
pip install -U yt-dlp
bash scripts/fetch_transcripts.sh "<PLAYLIST_OR_CHANNEL_URL>"
python3 scripts/clean_vtt.py transcripts/raw transcripts/clean
```

You end up with `transcripts/clean/01 - <title>.txt` … `37 - <title>.txt` —
readable prose with a timestamp every ~60 seconds.

Notes:
- Manual (creator-uploaded) captions are preferred automatically; auto-captions
  are the fallback. YouTube's ASR handles Rory's RP accent well — auto-captions
  are typically 95%+ accurate for him.
- If YouTube rate-limits you (HTTP 429), add `--sleep-requests 2` or
  `--cookies-from-browser chrome` to the script.

### Step 2 (optional) — Whisper for near-perfect accuracy

Only needed if a video has no captions or you want publication-grade text:

```bash
yt-dlp -f bestaudio -x --audio-format m4a -o "audio/%(playlist_index)02d - %(title)s.%(ext)s" "<PLAYLIST_URL>"
pip install faster-whisper
# then transcribe with model large-v3 (free on a Google Colab T4 GPU: ~5 min per hour of audio)
```

### Step 3 — Deep analysis with a frontier model

Feed the **full cleaned transcripts** (not snippets) to Claude or Gemini:

- **Per-video pass:** run `prompts/01-per-video-analysis.md` on each transcript.
  One video per conversation/message so the model reads it end-to-end.
- **Corpus synthesis pass:** concatenate the 37 per-video analyses and run
  `prompts/02-corpus-synthesis.md` over them to get the cross-video map of
  Sutherland's system of thought.

Fastest ways to execute this:
- **Claude Code** (this tool, on your own machine where YouTube isn't blocked):
  point it at the `transcripts/clean/` folder and ask it to run prompt 01 on
  every file and then prompt 02 — it loops automatically.
- **Claude Projects / Gemini AI Studio:** paste transcripts in batches.
  A typical 15-minute talk is ~2,500 words ≈ 3.5k tokens, so all 37 videos
  (~130k tokens) fit inside a single 200k–1M context window for the synthesis
  pass.

### No-code fallback (if you won't touch a terminal)

- **Gemini in AI Studio** accepts YouTube URLs directly — use
  `prompts/03-gemini-transcript-extraction.md` per video. Verbatim fidelity is
  good but not guaranteed; spot-check quotes.
- Browser tools like **NoteGPT / Tactiq / downsub.com** export the caption
  track per video — accurate but one-video-at-a-time (37 manual passes).

## Files

| Path | Purpose |
|---|---|
| `scripts/fetch_transcripts.sh` | Batch-download all captions from the playlist |
| `scripts/clean_vtt.py` | Convert rolling `.vtt` captions into clean readable text |
| `prompts/01-per-video-analysis.md` | The deep-analysis prompt (per video) |
| `prompts/02-corpus-synthesis.md` | Cross-video synthesis prompt (all 37) |
| `prompts/03-gemini-transcript-extraction.md` | No-code transcript extraction via Gemini |
