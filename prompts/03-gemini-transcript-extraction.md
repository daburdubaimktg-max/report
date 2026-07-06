# Prompt 03 — No-code transcript extraction (Gemini AI Studio)

Gemini in [AI Studio](https://aistudio.google.com) can ingest a YouTube URL
directly (paste the URL into the prompt). Use this per video when you can't
run yt-dlp. Verbatim fidelity is good but not guaranteed — spot-check a few
quotes against the video.

---

Watch this video in full: {{youtube_url}}

Produce a complete, verbatim transcript of everything spoken, with these rules:

1. Transcribe EVERY spoken word from start to finish. Do not summarize,
   paraphrase, condense, or skip any section. If the video is long, continue
   until the end — never stop early with "..." or "[continues]".
2. Insert a timestamp in [mm:ss] format at every speaker change and at least
   once per minute of video.
3. Label speakers (e.g., RORY SUTHERLAND:, INTERVIEWER:) when more than one
   person speaks.
4. Preserve his exact wording, including asides, jokes, and digressions —
   do not clean up or formalize the language.
5. Mark inaudible passages as [inaudible mm:ss] rather than guessing.
6. After the transcript, add a "SPOT-CHECK" section listing the video's first
   and last spoken sentences, so I can verify completeness.

Output the transcript as plain text, no commentary before it.
