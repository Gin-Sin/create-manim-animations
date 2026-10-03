# Interactive animation

Distinguish live simulation, native scene interaction, and presenter-controlled playback before choosing a runtime.

## Interaction modes

**Native Python/OpenGL:** ManimGL supports interactive development; Manim Community exposes OpenGL interaction in supported environments. Inspect the installed version's examples and `interactive_embed` behavior. Native windows, event loops, and GPU support matter on headless hosts. A local Python scene is not a static site. Consult [ManimGL](https://github.com/3b1b/manim) and the selected [Community Scene API](https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html).

**Presentation control:** Manim Slides provides boundaries, loops, and presenter/browser playback. It suits advancing a lecture, not automatically computing arbitrary simulation states. Verify current render/convert commands in its [quickstart](https://manim-slides.eertmans.be/latest/quickstart.html).

**Live browser objects:** The example uses [manim-web](https://github.com/maloyan/manim-web), a community TypeScript implementation. It is not Python Manim Community executing inside GitHub Pages. Explain that distinction, pin the version, and inspect needed primitives. Do not assume complete API compatibility.

If the requirement specifically means executing Python Manim in a browser, investigate a supported browser-Python or hosted-server design rather than relabeling a port. Prototype rendering, fonts, and LaTeX support before promising it. GitHub Pages can be a frontend, but cannot run a Python backend.

## Model, view, transition

```text
input action -> validated next state -> animated transition -> settled view
                       |                                      |
                    invariants                         accessible text
```

The model defines operations and rejects invalid actions. It must not infer semantic state from pixels, colors, or incomplete animation callbacks. The view maps state to objects; the transition explains the change, including necessary intermediate states.

For paged allocation, model request tables, physical blocks, owners/reference counts, block size, lengths, and free capacity. Validate ownership, capacity, correct lookup, and atomic failure. Copy-on-write must copy, redirect, then write, preserving the sibling's data.

Commit valid state once and lock conflicting controls during its animation. On rendering failure, preserve the model and show its committed state in the fallback. Use `try/finally` so controls unlock. Deliberately reject or queue rapid input; do not race transitions against the same objects.

## Runnable browser starter

The [starter](../assets/interactive-starter/) pins `manim-web` 0.3.24 and esbuild 0.25.12, matching the worked project. It animates a dot to a selected position using real `Scene`, `Line`, `Dot`, `Text`, and `Shift` objects with HTML controls. It is a runtime example, not a paged-memory implementation.

Copy it to the target project, then:

```bash
npm ci
npm run build
python3 -m http.server 8000 --directory dist
```

The starter uses system serif/monospace families without bundled fonts. For production, add permitted CMU Serif and JetBrains Mono webfonts and load them before constructing canvas text. Share type roles/colors between film and playground even though their APIs differ.

Example browser calls in this version:

```javascript
const scene = new Scene(container, {
  width: container.clientWidth, height: 400,
  frameWidth: 12, frameHeight: 6,
  backgroundColor: "#000000", autoRender: false, autoResize: false,
});
await scene.play(new Shift(dot, { direction: [dx, 0, 0], duration: 0.7 }));
scene.render();
```

Python `run_time` differs from the browser's `duration`. Verify constructors using package exports/types and an actual browser render. Use consistent logical coordinates. Handle resize safely while animations hold references to objects; dispose old click targets, listeners, observers, and scenes on teardown.

Use semantic phases. Copy-on-write should show copied contents before the append so the preserved original is visible. For a pulse following multiple path segments, weight duration by distance to avoid speed jumps.

The [3Blue1Brown pattern catalog](3b1b-patterns.md) includes an interactive adaptation for each pattern: selected-item focus, representation toggles, transform sliders, matrix-cell inspection, score normalization, prefix accumulation, detail/overview switches, and window stepping. Preserve object identity across a control change, and derive all displayed intermediate states from the model. The gallery's Python scenes illustrate staging; they are not browser code and require explicit adaptation to the selected runtime.

## Bundling and lifecycle

Use a local build and lockfile, not an unpinned runtime CDN import. Test under `/repository-name/` as well as the domain root; chunks, fonts, equations, and workers need valid deployed paths.

The worked distribution included shader strings. Its esbuild setting `supported: { "template-literal": false }` preserved required escaping in generated code. Keep this tested configuration when reusing that version and verify behavior when upgrading. Preserve third-party notices, including dependencies embedded in the distributed library.

With `autoRender: false`, verify how `scene.play()` schedules frames and call `render()` after direct changes. Follow the library lifecycle rather than adding an unrelated loop. Diagnose missing graphics by distinguishing initialization failure, zero canvas dimensions, unrendered state, context loss, and import errors.

## Accessible controls and responsive layout

- Use labeled native inputs/buttons for keyboard access; pointer hit targets supplement them.
- Show textual state and operation results outside the canvas.
- Respect reduced motion by drawing the same valid final state immediately.
- Keep controls/text functional if WebGL or scene initialization fails.
- Distinguish in-progress, completed, and rejected actions in concise status text.
- Reflow dense diagrams on narrow screens; shrinking a desktop diagram can make it unreadable.

## Test motion and state

Test consequential model invariants without graphics. Then test both normal/reduced motion in a browser: value change, reset, boundary cases, resize, keyboard input, and domain failures such as a full pool.

Capture a frame during a transition and another after it; verify both movement and the final state. For WebGL, capture within an appropriate animation frame if the drawing buffer is not preserved. Static final screenshots alone do not verify animation.

Monitor console errors and failed resources. Confirm controls unlock after errors and resize/teardown does not leave duplicate scenes. Repeat relevant checks on the published build, where caching and subpaths differ.

The bundled `tests/browser_starter_check.py` exercises these core starter behaviors against a served URL. It requires Python Playwright, Pillow, and Chromium; run it from the skill directory with `python tests/browser_starter_check.py http://localhost:8000`. `CHROMIUM_PATH` can select an existing full Chromium executable. This smoke test covers the small starter, not the invariants of a future domain model.
