#!/usr/bin/env python3
"""Check shared narration metadata, WebVTT, and optional encoded stream durations.

Standard library only; --movie additionally requires ffprobe. This does not
transcribe audio, measure loudness, or recognize burned-in text.
"""
import argparse
import json
import math
import re
import subprocess
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def seconds(value):
    parts = value.split(":")
    require(len(parts) in (2, 3), f"Invalid VTT timestamp: {value}")
    result = 0.0
    for part in parts:
        result = result * 60 + float(part)
    require(math.isfinite(result) and result >= 0, "Invalid VTT time")
    return result


def parse_vtt(path):
    content = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    require(content.startswith("WEBVTT"), "Missing WEBVTT header")
    cues = []
    for block in re.split(r"\n\s*\n", content.strip())[1:]:
        lines = block.splitlines()
        if not lines or lines[0].startswith(("NOTE", "STYLE", "REGION")):
            continue
        if "-->" not in lines[0]:
            lines = lines[1:]  # Optional cue identifier.
        require(lines and "-->" in lines[0], "Invalid VTT cue")
        start, end = lines[0].split("-->", 1)
        cues.append({"start": seconds(start.strip()),
                     "end": seconds(end.strip().split()[0]),
                     "text": " ".join(line.strip() for line in lines[1:])})
    return cues


def interval(cue, label):
    start, end = cue["start"], cue["end"]
    require(all(isinstance(v, (int, float)) and not isinstance(v, bool)
                and math.isfinite(v) for v in (start, end)), f"{label}: invalid time")
    require(0 <= start < end, f"{label}: empty or reversed interval")
    return start, end


def validate(script, visual, report, transcript, vtt, tolerance=0.025):
    require(math.isfinite(tolerance) and tolerance >= 0, "Invalid tolerance")
    texts, speech = script["cues"], report["speech"]
    require(isinstance(texts, list) and texts and all(isinstance(t, str) and t.strip() for t in texts),
            "Canonical script must contain nonempty text cues")
    require(all(len(items) == len(texts) for items in (visual, speech, transcript, vtt)),
            "Cue count differs across outputs")
    lead, pause = script["speech_lead"], script["end_pause"]
    require(all(isinstance(v, (int, float)) and math.isfinite(v) and v >= 0 for v in (lead, pause)),
            "Speech lead and end pause must be nonnegative")
    previous = {"visual": 0.0, "speech": 0.0, "transcript": 0.0, "vtt": 0.0}
    for index, text in enumerate(texts):
        records = dict(zip(previous, (visual[index], speech[index], transcript[index], vtt[index])))
        times = {}
        for kind, cue in records.items():
            label = f"Cue {index + 1} {kind}"
            # VTT may wrap lines; normalize whitespace only, never wording.
            require(" ".join(cue["text"].split()) == " ".join(text.split()), f"{label}: text differs")
            start, end = interval(cue, label)
            require(start >= previous[kind] - tolerance, f"{label}: overlaps previous cue")
            previous[kind] = end
            times[kind] = (start, end)
        vs, ve = times["visual"]
        ss, se = times["speech"]
        require(abs(ss - vs - lead) <= tolerance, f"Cue {index + 1}: wrong speech lead")
        require(se + pause <= ve + tolerance, f"Cue {index + 1}: caption hold ends before speech/pause")
        require(speech[index].get("tempo", 1) == 1, f"Cue {index + 1}: speech accelerated; extend the visual hold")
        for kind in ("transcript", "vtt"):
            start, end = times[kind]
            require(abs(start - ss) <= tolerance and se - tolerance <= end <= ve + tolerance,
                    f"Cue {index + 1}: {kind} does not cover the utterance within its visual hold")
    return len(texts), max(previous.values())


def check_movie(path, required_end, tolerance):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                            check=True, capture_output=True, text=True)
    metadata = json.loads(result.stdout)
    video = [s for s in metadata["streams"] if s["codec_type"] == "video"]
    audio = [s for s in metadata["streams"] if s["codec_type"] == "audio"]
    require(len(video) == 1 and len(audio) == 1, "Expected one video and one narration audio stream")
    vd = float(video[0].get("duration", metadata["format"]["duration"]))
    ad = float(audio[0].get("duration", metadata["format"]["duration"]))
    require(required_end <= vd + tolerance, "Cue exceeds encoded video duration")
    require(abs(vd - ad) <= tolerance + 0.05, "Audio/video duration mismatch")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("script", "visual", "soundtrack", "transcript", "vtt"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    parser.add_argument("--movie", type=Path)
    parser.add_argument("--tolerance", type=float, default=0.025)
    args = parser.parse_args()
    try:
        documents = [json.loads(getattr(args, name).read_text())
                     for name in ("script", "visual", "soundtrack", "transcript")]
        count, end = validate(*documents, parse_vtt(args.vtt), args.tolerance)
        if args.movie:
            check_movie(args.movie, end, args.tolerance)
    except (ValueError, KeyError, TypeError, IndexError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"FAIL: {error}\n")
    print(f"PASS: {count} matching narration cues; timing, holds, transcript, and VTT agree."
          + (" Encoded stream durations agree." if args.movie else ""))


if __name__ == "__main__":
    main()
