#!/usr/bin/env python3
"""Convert YouTube .vtt caption files into clean, readable transcripts.

YouTube auto-captions use "rolling" cues: each caption line is repeated in the
next cue, and lines carry inline word-timing tags. This script strips the tags,
de-duplicates the rolling lines, and emits flowing text with a [mm:ss] marker
roughly every 60 seconds so quotes stay findable in the video.

Usage: python3 scripts/clean_vtt.py <input_dir> <output_dir>
"""
import re
import sys
from pathlib import Path

TAG_RE = re.compile(r"<[^>]+>")
TS_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.\d{3}\s+-->")
MARKER_INTERVAL = 60  # seconds between [mm:ss] markers


def clean_vtt(text: str) -> str:
    out, last_line, last_marker = [], None, -MARKER_INTERVAL
    cue_start = 0
    for raw in text.splitlines():
        line = raw.strip()
        m = TS_RE.match(line)
        if m:
            cue_start = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            continue
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        line = TAG_RE.sub("", line).replace("&nbsp;", " ").replace("&amp;", "&").strip()
        if not line or line == last_line:
            continue
        last_line = line
        if cue_start - last_marker >= MARKER_INTERVAL:
            h, rem = divmod(cue_start, 3600)
            mm, ss = divmod(rem, 60)
            stamp = f"[{h}:{mm:02d}:{ss:02d}]" if h else f"[{mm:02d}:{ss:02d}]"
            out.append(f"\n{stamp} ")
            last_marker = cue_start
        out.append(line + " ")
    return "".join(out).strip()


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    vtts = sorted(src.glob("*.vtt"))
    if not vtts:
        sys.exit(f"No .vtt files found in {src}")
    for vtt in vtts:
        # strip trailing language suffix like ".en" from the stem
        stem = re.sub(r"\.[a-z]{2}(-[A-Za-z]+)?$", "", vtt.stem)
        out_path = dst / f"{stem}.txt"
        out_path.write_text(clean_vtt(vtt.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"{vtt.name} -> {out_path}")
    print(f"\n{len(vtts)} transcript(s) written to {dst}/")


if __name__ == "__main__":
    main()
