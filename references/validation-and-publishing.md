# Validation and publishing

Apply only checks relevant to requested modes. A silent film does not require a speech pipeline; a local scene does not require deployment.

## Validate actual artifacts

For films, probe dimensions, frame rate, codecs, stream count, and durations. Inspect full-resolution frames at caption changes, dense equations, long labels, and settled states. Watch difficult transitions; smooth motion can still communicate the wrong model.

For narration, compare canonical text, rendered metadata, speech provenance, VTT, and transcript. Verify lead/hold timing, audibility, loudness, peaks, and complete endings. OCR can detect stale rendered text, but adapt its crop/language to the actual film and inspect failures rather than weakening the comparison.

The bundled `scripts/check_narration.py` supports any nonempty cue count and can probe media with FFprobe. It does not measure loudness, transcribe recordings, or OCR frames. Test a changed sentence, insufficient hold, and overlapping cues to ensure it rejects meaningful failures; avoid tests that merely search source code for function names.

Run the bundled checker's regression tests from this skill directory with `python3 -m unittest discover -s tests -v`.

For playgrounds, test model invariants plus actual normal/reduced-motion behavior, keyboard controls, narrow/wide layouts, unavailable graphics, reset, and consequential boundaries. A playable video and operational canvas are separate acceptance criteria.

## Reproducible layout

```text
scenes/                    Python Manim source
audio/narration.json        Canonical script
audio/voice/                Optional checked-in speech cache
web/                       Browser scene source
scripts/                   Build/render/mix/preview commands
tests/                     Model and artifact checks
docs/                      Static deployment root
docs/assets/               MP4, metadata, fonts, math, browser bundle
media/                     Ignored intermediate renders/stems
```

Create only needed directories. Pin dependencies and record runtime versions. Store speech clips if offline rebuilding and redistribution are appropriate; otherwise document regeneration. Exclude environments, `node_modules`, credentials, intermediate WAVs, and review screenshots by default.

Check media against current repository/hosting constraints before pushing. If too large, use an authorized supported media/download arrangement; do not silently omit the film. Keep font and bundled-library notices. Avoid unrelated WOFF2 churn from timestamp-only regeneration when changing narration.

## Static website

Use `<video controls playsinline preload="metadata">` with MP4, poster, caption track, and download fallback. Generate chapter/transcript seeking from metadata. Let the viewer initiate sound; do not depend on autoplay with audio.

Preview video on an HTTP server supporting byte ranges. `file://` does not reproduce deployed module/fetch/media behavior. Use relative URLs or a configured base path: GitHub project sites usually live under `/repository/`.

Update content hashes/cache versions for video, VTT, chapters, transcript, and loading code together after timing edits. Remove stale manually written durations.

## Push and deploy when authorized

Check the remote, account, branch, visibility, and working tree. Reuse the user's chosen repository. Resolve consequential visibility uncertainty before publishing. Do not push unrelated work or force-push an ordinary update.

A new-repository example, substituting agreed visibility and actual paths:

```bash
git init -b main
git add <explicit-deliverable-paths>
git commit -m "Add explanatory Manim film and interactive playground"
gh repo create OWNER/REPOSITORY --public --source . --remote origin --push
```

Inspect partial success before retrying creation/push. Repeated permission/authentication failure should be reported; do not create duplicate repositories or repeatedly mutate settings.

For Pages Actions, use checkout → install locked dependencies → check model → build browser assets → check media → configure Pages → upload static directory → deploy. Give the workflow appropriate Pages/OIDC permissions and verify current action versions/settings using [GitHub's workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

If the repository publishes pre-rendered media, deploying need not re-run expensive Manim rendering. If CI does render, explicitly provision fonts, LaTeX, FFmpeg, and audio dependencies. Unchanged cached narration should not require new online synthesis just to redeploy.

## Verify the live version

Wait for deployment of the pushed commit, not an older successful run. Verify:

- The expected asset version is served; compare hashes when useful.
- Video plays, seeks to generated chapter boundaries, and produces initiated audio.
- Captions/transcript match the deployed movie.
- The scene initializes, responds, and animates under the deployed subpath.
- Fonts, math, and split JavaScript chunks load without errors.

If blocked, finish the local artifact and report the exact deployment obstacle. On success, provide the GitHub/live link and relevant validation without internal logs or credentials.
