# Film and visual design

Read the narration guide before finalizing durations for a voiced film.

## Environment and runtime

Determine whether the project imports `manim` (Community) or `manimlib` (ManimGL). Do not mix their examples without adapting APIs. Inspect the installed version, renderer, Python environment, FFmpeg, LaTeX/dvisvgm, and fonts.

```bash
python -m manim --version
ffmpeg -version
ffprobe -version
latex --version
dvisvgm --version
fc-match 'CMU Serif'
fc-match 'JetBrains Mono'
```

Use an isolated environment and record dependencies. Install native Cairo/Pango/LaTeX packages only as required by the selected runtime. Avoid upgrading the whole environment to repair one missing font. Check version-specific documentation and installed source when an API is uncertain.

The worked project used Manim Community 0.19.0. This is a reproducibility reference, not a requirement or a claim about the latest release. [Manim Community](https://docs.manim.community/en/stable/) and [ManimGL](https://github.com/3b1b/manim) are separate projects.

## Storyboard operations and invariants

For each chapter, record the viewer's question, the conclusion, the objects that enter/persist, the operation, a numeric example, an invariant, and its narration cue. Tie motion and sound to meaningful events.

A useful PagedAttention sequence is KV cache → wasted reservation → logical/physical mapping → unchanged attention mathematics → allocation → sharing/copy-on-write. This is an example, not a mandatory six-chapter structure.

Keep examples mentally checkable. For zero-based tokens, six existing tokens occupy indices 0–5; appending the next writes index 6. Preserve this distinction in speech, code, and diagrams. Establish domain correctness before animating it.

## Typography

| Role | Example | Implementation |
| --- | --- | --- |
| Narration and explanatory labels | CMU Serif | `Text(..., font="CMU Serif")` |
| Code and physical addresses | JetBrains Mono | `Text(..., font="JetBrains Mono")` or the selected version's `Code` |
| Mathematics | Computer Modern through LaTeX | `MathTex` / `Tex` |
| Website controls | Lato or another readable UI family | CSS |

Set families explicitly. `fc-match` can return a fallback; inspect the family it actually resolves. Check minus signs, Greek letters, subscripts, ligatures, apostrophes, brackets, and literal code punctuation. Keep code whitespace.

Wrap prose at meaningful boundaries and measure width. Do not shrink an overflowing caption until it becomes unreadable. Reserve a caption band outside the diagram/equation area. Review the longest sentence and caption overlays at final viewing size.

For browser graphics, load required webfonts before creating canvas text and await `document.fonts.ready`. A font loaded later can leave stale label metrics. Bundle permitted fonts and notices to avoid dependence on viewer-installed families.

## Equations and patterns

Use actual mathematical typesetting:

```python
rule = MathTex(
    r"b=\left\lfloor\frac{t}{B}\right\rfloor",
    r",\qquad",
    r"r=t\bmod B",
)
```

Separate formula tokens where a transformation should preserve identity. Use `TransformMatchingTex` for meaningful symbolic correspondence and verify the rendered match. A clean replacement is better than a misleading morph.

Prefer data-shaped primitives: vectors, aligned rows, braces, memory strips, arrows, and sparse tables. Use constructors for repeated blocks and labels so baselines, stroke weights, and cell sizes remain consistent. Carry semantic colors across equivalent representations. Route arrows through clear space rather than labels.

When using a 3Blue1Brown reference, identify concrete properties: serif proportion, formula scale, stroke weight, introduction order, camera framing, and continuity. Create an original explanation using these principles. Do not claim that Manim alone reproduces the reference's quality.

For concrete choices, use the [3Blue1Brown pattern catalog](3b1b-patterns.md). It maps timestamped examples to nine original runnable scenes in `assets/pattern_gallery.py`, with staging, timing, failure modes, and interactive variants. The [source notes](3b1b-source-notes.md) record how each reference was checked.

## Scene and timing structure

Separate domain calculations, graphical primitives, chapter construction, and exported metadata. A chapter base class can own the title, narration band, cue times, and review markers.

Record actual renderer time at cue starts, semantic events, and chapter ends. Probe encoded chapter durations to compute assembled offsets. At 60 fps a frame is about 16.7 ms; account for frame quantization when comparing times.

For a two-second visual operation and a seven-second sentence, animate the operation and hold its useful final state until the voice finishes. When a clause refers to a precise event, use deliberate intermediate holds or word/bookmark timing. Sentence agreement alone does not align every action to the intended word.

## Rendering and review

```bash
python -m manim -ql --fps 30 scenes/explanation.py Mapping
python -m manim -qh --fps 60 scenes/explanation.py Mapping
```

Render the difficult scene, then a full draft. Inspect caption changes, dense equations, completed transitions, and long labels. Watch movement; stills cannot reveal abrupt or misleading transformations.

Use consistent resolution and frame rate for assembly. H.264, `yuv420p`, AAC, and MP4 `+faststart` worked for browser delivery in the example. Re-encode when chapters cannot safely concatenate without it. Preserve a silent render when useful for audio-only rebuilds.

When external script/timing files change, confirm cached frames are not stale; invalidate affected caches if needed. After timing edits, regenerate chapters, captions, transcript links, poster timing, and effect anchors together.
