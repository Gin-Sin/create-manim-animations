# Worked example: PagedAttention

This skill was distilled from [ML System Illustrations](https://github.com/Gin-Sin/ml-system-illustrations/tree/bc3b620e2ceb31c44c96513bf13d08c6b4341b2f). The [published film and playground](https://gin-sin.github.io/ml-system-illustrations/?v=5#film) show the result. The pinned commit preserves the described implementation if the live site changes.

## Deliverables and model

The project contains a six-chapter Python Manim Community film at 1080p60, a `manim-web` playground, narration/effects, captions/transcript, and Pages deployment. CMU Serif, JetBrains Mono, and LaTeX distinguish prose, code, and mathematics.

The mapping example uses block size `B = 4`, token index `t = 6`, and `table[1] = 2`:

```text
b = floor(t / B) = 1
r = t mod B = 2
physical block = table[b] = 2
resolved block/slot = P2[2]
```

This is logical address resolution, not an actual byte-address calculation. For requests with 6, 3, and 5 tokens, reserving 12 slots each uses 14 of 36 reserved slots. Whole blocks of four need `8 + 4 + 8 = 20` slots for those 14 tokens. Tail slack remains; paging does not eliminate all unused capacity.

The attention view shows one head and shared softmax normalization across valid keys. Physical page boundaries must not imply separate denominators. Complete prefix blocks remain shared; a shared partial tail is copied before appending. A full tail can instead be followed by a new block. Release frees a block only after its final reference disappears.

## Narration failure and correction

Initially, shorter spoken paraphrases were added to a film with longer burned-in narration. Captions/transcript matched the voice, but the visible narration differed. Metadata checks limited to subtitles could not detect that.

The repair made `audio/narration.json` canonical for speech, Manim text, VTT, and transcript. The pipeline generated/measured full utterances first, extended scene holds, and rejected stale text or insufficient time. The film grew to about 166 seconds instead of accelerating the voice.

All twenty passages were checked, actual caption frames were OCR-read, encoded audio was measured, and browser playback, seeking, interaction, and deployment were verified. The reusable lesson is shared text and measured timing, not the particular cue count or voice.

## Source map

Paths are relative to the pinned repository:

| File | Technique |
| --- | --- |
| `scenes/paged_attention.py` | Semantic objects, type roles, canonical cue references, measured holds |
| `scripts/build_audio.py` | Cached clips, prepared durations, natural-speed speech, effects, ducking, normalization, muxing |
| `scripts/render.py` | Chapter assembly, duration probing, generated metadata/poster |
| `scripts/build_typography.py` | Local webfonts and equation SVGs |
| `docs/allocator.js` | Domain operations independent of graphics |
| `web/playground.js` | Live browser objects, phased transitions, resizing, hit targets, disposal |
| `scripts/build_web.mjs` | Pinned bundling, shader escaping, dependency notices |
| `tests/allocator.test.js` | Lookup/allocation/sharing/release and atomic failure |
| `tests/audio_check.py` | Audible speech, provenance, timing, encoded loudness |
| `tests/caption_frames.py` | OCR of burned-in narration |
| `tests/browser_check.py` | Motion, controls, fallback, fonts, responsiveness, audio, seeking |
| `.github/workflows/pages.yml` | Validate/build/publish |

Tested baseline: Manim Community 0.19.0; edge-tts 7.2.8; fonttools 4.66.1; manim-web 0.3.24; esbuild 0.25.12; Node 22 for the web build. These pins describe a working snapshot, not the latest releases.
