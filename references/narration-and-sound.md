# Narration and sound

Prevent independently authored spoken and on-screen narration. Metadata agreement is necessary but does not replace checking the actual recording and frames.

## Canonical script

The bundled example and checker use:

```json
{
  "voice": "en-US-AndrewNeural",
  "rate": "-8%",
  "speech_lead": 0.4,
  "end_pause": 0.5,
  "cues": ["The exact sentence shown and spoken."]
}
```

The voice and margins are examples, not universal requirements. Derive burned-in narration, TTS input, VTT, and transcript from `cues`. Titles and labels are separate. If the user wants a shorter on-screen summary, model it deliberately as a separate field rather than accidentally paraphrasing matching narration.

An indexed list works for a short fixed sequence. Stable named cue IDs help larger editable projects; adapt the checker if adopting that schema. For recorded human speech, retain the intended text and verify what was actually spoken.

## Prepare speech first

1. Generate complete cues separately. Cache by engine/version, voice, rate, text, and every setting that changes output. Text edits must invalidate their clips.
2. Write a temporary file, verify it decodes, then replace the cache entry. Use bounded retries for transient errors. Repeated authentication/quota errors require another available route or a clear report, not indefinite retries.
3. Decode to a common format, such as 48 kHz mono float PCM. Trim only surrounding silence with consonant/breath margins. Preserve internal pauses and complete words.
4. Measure the samples that will actually be mixed. Duration is sample count divided by sample rate; do not estimate it from word count.
5. Write timing metadata and make Manim reject stale text, voice, or rate before rendering.

The template reads `media/audio/narration-timing.json`:

```json
{
  "voice": "en-US-AndrewNeural",
  "rate": "-8%",
  "cues": [{"text": "The exact sentence shown and spoken.", "duration": 3.2}]
}
```

Reuse the project's speech provider. The worked implementation used [edge-tts](https://github.com/rany2/edge-tts), an optional choice rather than a guarantee of service availability. Cached clips permit offline rebuilding. Preserve synthesis provenance and keep credentials outside published artifacts.

## Hold text through the utterance

For caption start `c`, speech lead `L`, measured duration `D`, and trailing pause `P`:

```text
speech_start = c + L
speech_end = speech_start + D
caption_end >= speech_end + P
```

Before replacing a caption or ending a chapter, wait for any remaining duration rounded upward to frames:

```python
remaining = required_end - float(self.renderer.time)
if remaining > 0:
    self.wait(math.ceil(remaining * config.frame_rate) / config.frame_rate)
```

Finish holding the **previous** cue before assigning the next cue. Protect the chapter's final cue as well. Start speech after fade-in; the worked project pairs a 0.4-second lead with a 0.35-second fade.

`assets/timed_scene.py` implements this pattern and exports local cue times. Copy `assets/narration.example.json` into a new project's `audio/narration.json`, prepare measured timing metadata, and render `SharedScriptDemo`. The template requires CMU Serif and JetBrains Mono; explicitly change their roles if unavailable. It is a visual timing scaffold, not a speech generator or mixer.

If speech is too long, extend holds or revise the shared sentence and rebuild both outputs. Do not shorten only the voice or silently speed it up. An audio-only rebuild should reject differences from the already-rendered text and insufficient visual time.

## Assembled metadata

Probe chapter durations and add their offsets to local cue times. Export:

- `visual-cues.json`: a list of `{start, end, text}` for on-screen narration.
- `soundtrack.json`: a `speech` list with `{start, end, text, tempo}` plus optional clip `source`; record voice provenance and effects too.
- `transcript.json`: the spoken text with navigation intervals.
- `captions.vtt`: the same spoken text in WebVTT intervals.

Example validation command, adjusted to project paths:

```bash
python /path/to/create-manim-animations/scripts/check_narration.py \
  --script audio/narration.json \
  --visual docs/assets/visual-cues.json \
  --soundtrack docs/assets/soundtrack.json \
  --transcript docs/assets/transcript.json \
  --vtt docs/assets/captions.vtt \
  --movie docs/assets/paged-attention.mp4
```

The checker allows 0.025 seconds of rounding by default; adapt to the actual frame rate. It checks metadata and basic encoded stream properties. It does not transcribe speech or read frames. Retain clip provenance, inspect/OCR frames when needed, and listen before claiming full agreement.

## Effects and mixing

Anchor sounds to recorded semantic events: allocation, write, lookup arrival, copy completion, and release. Cue-relative offsets suit stable short operations; recheck them after motion edits. Whole-film hardcoded offsets drift when earlier chapters lengthen.

Quiet synthesized ticks, brief tones, and filtered noise sweeps can distinguish operations. Add short fades to prevent clicks. Keep effects below narration and duck them during speech. Seed generated noise for reproducibility. Panning may reinforce movement, but mono playback should still convey the explanation. Retain permission/source records for external audio.

Keep separate speech/effect stems. Normalize speech, mix, and measure the encoded result. A useful speech-led web-film starting point is roughly −16 LUFS integrated stereo with a true-peak target near −1.5 dBTP. These are production choices, not universal specifications. A measured two-pass FFmpeg `loudnorm` workflow gives more predictable levels; AAC can change peak levels, so check after encoding.

For audio-only assembly, mux a prepared WAV with `-c:v copy`, AAC at 48 kHz, the intended duration, and `-movflags +faststart`. Verify no accidental second audio stream, clipped ending, silent cue, or drift.

Listen to the introduction, longest sentence, code/math passage, chapter transitions, and ending. Check index/abbreviation pronunciation. If a pronunciation expansion is necessary, tie it explicitly to the canonical cue and verify the spoken meaning; do not introduce a separate shortened script.

After a timing edit, replace all dependent metadata and update cache hashes/versions together. A new MP4 paired with an old transcript remains a broken delivery.
