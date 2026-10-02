---
name: create-manim-animations
description: Create and refine explanatory Manim films and interactive Manim demonstrations, including typography, equations, synchronized narration, sound effects, browser playgrounds, and optional GitHub Pages delivery. Use for Manim animation work, not ordinary charts or general website development.
---

# Create Manim Animations

Produce an explanation whose geometry, equations, motion, and spoken words describe the same model. Deliver editable source and the requested rendered or interactive experience. A film request does not automatically require a playground, narration, or deployment; select applicable modes.

## Choose the deliverable and runtime

Infer the concept, audience, target duration, output format, existing project, and delivery location from the conversation and repository. Ask only about consequential missing choices. Inspect existing instructions and preserve unrelated changes.

| Experience | Suitable approach | Viewer interaction |
| --- | --- | --- |
| Explanatory video | Python Manim Community, or the project's existing ManimGL runtime | Playback and seeking |
| Native live mathematical scene | ManimGL, or supported Manim Community OpenGL interaction | Change scene state in a desktop runtime |
| Presenter-controlled sequence | Manim Slides | Advance, reverse, or loop rendered sections |
| Stateful playground on a static website | A verified browser runtime such as `manim-web` | Change parameters and live graphical objects |

These runtimes have different APIs. Do not silently replace a requirement for Python Manim with a browser port. For a GitHub Pages playground, disclose that `manim-web` is a community TypeScript port and verify it satisfies the intended interaction. A video scrubber is not an arbitrary-state simulation. Static hosting does not provide a running Python/OpenGL server.

Read only the relevant guides:

- [Film and visual design](references/film-and-design.md): storyboard, setup, typography, equations, scenes, and rendering.
- [Narration and sound](references/narration-and-sound.md): canonical script, measured speech, holds, effects, mixing, and captions.
- [Interactive animation](references/interactive-animation.md): native/browser choices, state transitions, lifecycle, accessibility, and runnable starter.
- [Validation and publishing](references/validation-and-publishing.md): artifact review, interaction checks, reproducibility, and GitHub Pages.
- [Worked PagedAttention example](references/paged-attention-example.md): domain checks, demonstrated failures, tested versions, and source links.

## Build around an explanation

1. Write the causal story: the question, the objects, the operation that changes them, and the invariant that survives. Choose a small numeric example. Distinguish illustrative simplifications from real-system claims.
2. Define reusable objects and semantic colors. Equivalent data in different representations should retain its identity; reserve a highlight for the current operation.
3. Establish separate type roles for narrative, code/addresses, mathematics, and controls. Narrative and code must look distinct. Typeset equations properly and preserve their meaning during transformations.
4. Build a representative difficult scene first. Inspect actual frames at the intended size, including its longest caption and densest equation. Resolve collisions and unreadable text before expanding the film.
5. Render a draft, inspect motion and stills, then render delivery quality. Derive timing metadata from the rendered timeline rather than manually maintained offsets.

For a 3Blue1Brown reference, study introduction order, equation-to-object correspondence, restrained color, serif typography, and purposeful continuity. A black background alone does not deliver that explanatory quality. Create original scenes; visual inspiration does not imply imitating a person's voice.

## Keep narration exact and timed

When text is presented as on-screen narration, generate it, the spoken passage, closed captions, and transcript from **one canonical text field**. Titles, labels, and deliberately shorter summaries have separate roles and need not be read aloud. Never maintain an independent shortened voice script for text intended to match it.

Prepare and measure speech before final scene timing. Start speech after its caption appears; hold the caption until the entire utterance and a trailing pause finish. If speech is too long, extend the scene or revise the shared sentence and rebuild all outputs. Do not silently cut words, paraphrase, or accelerate speech to fit an old render.

Adapt [assets/timed_scene.py](assets/timed_scene.py) and [assets/narration.example.json](assets/narration.example.json) for a small Manim Community example. The audio guide defines the prepared timing contract. This template does not itself synthesize or mux audio.

Run [scripts/check_narration.py](scripts/check_narration.py) against final metadata and VTT. It detects text drift, overlap, and insufficient holds. It cannot prove that a recording contains the expected words: retain synthesis provenance, inspect the encoded film, and listen to representative passages.

## Make interaction change the model

Use a state model that can be validated without graphics. An action computes a valid next state; the scene animates the transition; the final graphics and accessible text represent the committed state. Keep domain invariants independent of animation callbacks.

For browser work, adapt [assets/interactive-starter/](assets/interactive-starter/). It contains a real `manim-web` scene, native controls, motion, reduced-motion support, resizing, and a text fallback. Replace its small position model with the requested concept.

Inspect an intermediate animated frame as well as the final result. Exercise rapid input, reset, boundaries, keyboard controls, mobile layout, and unavailable graphics as applicable. A canvas displaying a final state alone does not prove animation ran.

## Finish and deliver

Validate what the user consumes: encoded media, captions, visible text, browser interaction, and published paths. Keep reproducible source, dependency pins, necessary generated assets, and redistribution notices. Exclude environments, credentials, caches, and transient review files.

Push and deploy when the conversation authorizes it; this skill does not independently grant permission to publish. Do not request authorization already provided. Verify the deployment associated with the pushed commit and the served version, not merely a successful push.

Report the artifact/live URL, interaction runtime, relevant checks, and remaining limitations.
