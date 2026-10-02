"""Manim Community visual scaffold; prepare measured speech before rendering.

From the target project root:
  python -m manim -ql path/to/timed_scene.py SharedScriptDemo

Reads audio/narration.json and media/audio/narration-timing.json.
Exports scene-local visual cue times. Synthesis and final audio muxing are separate.
"""
import json
import math
import textwrap
from pathlib import Path

from manim import (
    Scene, Text, MathTex, VGroup, FadeIn, FadeOut, Write,
    UP, DOWN, LEFT, RIGHT, config,
)


class TimedChapter(Scene):
    narrative_font = "CMU Serif"
    code_font = "JetBrains Mono"

    def setup(self):
        self.script = json.loads(Path("audio/narration.json").read_text())
        prepared = json.loads(Path("media/audio/narration-timing.json").read_text())
        if [cue["text"] for cue in prepared["cues"]] != self.script["cues"]:
            raise ValueError("Prepared speech text is stale; regenerate before rendering.")
        if any(prepared[key] != self.script[key] for key in ("voice", "rate")):
            raise ValueError("Prepared voice settings are stale.")
        self.durations = [cue["duration"] for cue in prepared["cues"]]
        if not all(isinstance(t, (int, float)) and math.isfinite(t) and t > 0 for t in self.durations):
            raise ValueError("Prepared speech durations must be positive and finite.")
        self.camera.background_color = "#000000"
        self.active = None
        self.caption_object = None
        self.cues = []

    def finish_cue(self):
        if self.active is None:
            return
        end = self.started + self.script["speech_lead"] + self.durations[self.active] + self.script["end_pause"]
        remaining = end - float(self.renderer.time)
        if remaining > 1e-6:
            self.wait(math.ceil(remaining * config.frame_rate) / config.frame_rate)
        self.cues.append({"start": self.started, "end": float(self.renderer.time),
                          "text": self.script["cues"][self.active]})
        self.active = None

    def caption(self, index):
        self.finish_cue()
        self.active, self.started = index, float(self.renderer.time)
        text = textwrap.fill(self.script["cues"][index], width=80, break_long_words=False)
        caption = Text(text, font=self.narrative_font, font_size=25, line_spacing=0.8)
        if caption.width > config.frame_width - 1:
            caption.scale_to_fit_width(config.frame_width - 1)
        caption.to_edge(DOWN, buff=0.25)
        fade = min(0.35, self.script["speech_lead"])
        if fade > 0:
            animations = [FadeIn(caption)]
            if self.caption_object is not None:
                animations.append(FadeOut(self.caption_object))
            self.play(*animations, run_time=fade)
        else:
            if self.caption_object is not None:
                self.remove(self.caption_object)
            self.add(caption)
        self.caption_object = caption

    def finish(self):
        self.finish_cue()
        output = Path("media/timings")
        output.mkdir(parents=True, exist_ok=True)
        (output / f"{type(self).__name__}.json").write_text(json.dumps(self.cues, indent=2) + "\n")


class SharedScriptDemo(TimedChapter):
    def construct(self):
        if len(self.script["cues"]) != 2:
            raise ValueError("This small demonstration expects the two example cues; adapt the scene for a new script.")
        heading = Text("What does a token leave behind?", font=self.narrative_font, font_size=38).to_edge(UP)
        self.play(FadeIn(heading))
        self.caption(0)
        key = MathTex(r"\mathbf{k}_0", color="#58C4DD").scale(1.5)
        value = MathTex(r"\mathbf{v}_0", color="#5CD0B3").scale(1.5)
        pair = VGroup(key, value).arrange(DOWN, buff=0.5).shift(LEFT * 2)
        label = Text("token[0]", font=self.code_font, font_size=25).next_to(pair, UP)
        self.play(Write(pair), FadeIn(label), run_time=1.5)
        self.caption(1)
        next_pair = VGroup(MathTex(r"\mathbf{k}_1", color="#58C4DD"),
                           MathTex(r"\mathbf{v}_1", color="#5CD0B3")).scale(1.5).arrange(DOWN, buff=0.5).shift(RIGHT * 2)
        next_label = Text("token[1]", font=self.code_font, font_size=25).next_to(next_pair, UP)
        self.play(FadeIn(next_pair), FadeIn(next_label), run_time=1.5)
        self.finish()
