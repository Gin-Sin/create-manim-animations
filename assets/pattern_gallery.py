"""Nine original Manim Community staging studies; see references/3b1b-patterns.md.

Render named scenes with: python -m manim -ql --fps 30 pattern_gallery.py OneThenMany
Silent examples, not copies of 3Blue1Brown scenes or a narrated final film.
Requires CMU Serif, JetBrains Mono, and LaTeX. Tested with Manim Community 0.19.0.
"""
import json
from pathlib import Path

import numpy as np
from manim import (
    Scene, Text, MathTex, Matrix, VGroup, NumberPlane, Arrow, Dot, Line,
    Rectangle, SurroundingRectangle, Brace, DecimalNumber,
    FadeIn, FadeOut, GrowArrow, Create, Write, LaggedStart, AnimationGroup,
    ReplacementTransform, Transform, TransformFromCopy, ApplyMatrix, Indicate,
    UP, DOWN, LEFT, RIGHT, ORIGIN, config,
)

INK, MUTED, BLUE, TEAL, GOLD = "#F5F3EF", "#777777", "#58C4DD", "#5CD0B3", "#FFFF80"


def prose(text, size=27, color=INK):
    return Text(text, font="CMU Serif", font_size=size, color=color)


def code(text, size=23, color=INK):
    return Text(text, font="JetBrains Mono", font_size=size, color=color)


def math(text, color=INK, size=35):
    return MathTex(text, color=color, font_size=size)


class PatternScene(Scene):
    def setup(self):
        self.camera.background_color = "#000000"
        self.marks = []

    def intro(self, title, explanation):
        heading = prose(title, 35).to_edge(UP, buff=0.35)
        if heading.width > 12.5:
            heading.scale_to_fit_width(12.5)
        note = prose(explanation, 23).to_edge(DOWN, buff=0.28)
        if note.width > 12.5:
            note.scale_to_fit_width(12.5)
        self.play(FadeIn(heading), FadeIn(note), run_time=0.6)

    def mark(self, name):
        self.marks.append({"name": name, "time": float(self.renderer.time)})

    def finish(self):
        self.mark("final")
        self.wait(1.2)

    def tear_down(self):
        output = Path(config.media_dir) / "pattern-review"
        output.mkdir(parents=True, exist_ok=True)
        (output / f"{type(self).__name__}.json").write_text(json.dumps(self.marks, indent=2) + "\n")


class OneThenMany(PatternScene):
    def construct(self):
        self.intro("One operation, then the collection", "Each input has its own result; the operation is shared.")
        inputs, arrows, maps, outputs = [], [], [], []
        for i, x in enumerate([-4.5, -1.5, 1.5, 4.5]):
            inputs.append(math(rf"\mathbf{{e}}_{i}", BLUE).move_to([x, 1.5, 0]))
            arrows.append(Arrow([x, 1.0, 0], [x, -0.55, 0], buff=0, color=MUTED))
            maps.append(math(r"W_Q", GOLD, 27).move_to([x + .5, .2, 0]))
            outputs.append(math(rf"\mathbf{{q}}_{i}", TEAL).move_to([x, -1.05, 0]))
        for item in inputs[1:]:
            item.set_opacity(.25)
        self.play(*[FadeIn(item) for item in inputs], run_time=.6)
        self.play(GrowArrow(arrows[0]), FadeIn(maps[0]), FadeIn(outputs[0]), run_time=1.1)
        self.mark("single")
        self.wait(.7)
        self.play(*[item.animate.set_opacity(1) for item in inputs[1:]], run_time=.4)
        self.play(LaggedStart(*[
            AnimationGroup(GrowArrow(arrows[i]), FadeIn(maps[i]), FadeIn(outputs[i]))
            for i in range(1, 4)
        ], lag_ratio=.2), run_time=1.4)
        self.finish()


class ArrowsToPoints(PatternScene):
    def construct(self):
        self.intro("A simpler mark, the same object", "Every dot stays at the endpoint of its corresponding arrow.")
        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-2, 2, 1], x_length=8, y_length=4)
        plane.set_stroke(color=MUTED, opacity=.3, width=1)
        points = [np.array([x, y, 0.0]) for y in (-1.5, -.5, .5, 1.5) for x in (-3, -1, 1, 3)]
        selected = 10
        arrows = [Arrow(ORIGIN, p, buff=0, color=GOLD if i == selected else BLUE,
                        stroke_width=2).set_opacity(1 if i == selected else .45) for i, p in enumerate(points)]
        dots = [Dot(p, radius=.07, color=GOLD if i == selected else BLUE) for i, p in enumerate(points)]
        self.add(plane)
        self.play(*[GrowArrow(a) for a in arrows], run_time=.8)
        self.mark("arrows")
        self.play(Indicate(arrows[selected], color=GOLD), run_time=.6)
        self.play(*[ReplacementTransform(a, d) for a, d in zip(arrows, dots)], run_time=1.0)
        self.mark("points")
        transform = np.array([[1, .45], [0, 1]])
        targets = [np.r_[transform @ p[:2], 0] for p in points]
        self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], run_time=1.6)
        self.finish()


class ReferenceGrid(PatternScene):
    def construct(self):
        self.intro("Keep a fixed reference", "The faint grid stays put while the foreground is sheared.")
        base = NumberPlane(x_range=[-4, 4, 1], y_range=[-2, 2, 1], x_length=8, y_length=4)
        base.set_stroke(color="#999999", opacity=.4, width=1)
        moving = base.copy().set_stroke(color=BLUE, opacity=.75, width=1.5)
        vector = Arrow(ORIGIN, [1, 1, 0], buff=0, color=GOLD)
        ghost = vector.copy().set_opacity(.35)
        self.play(Create(base), run_time=.5)
        self.play(Create(moving), GrowArrow(vector), run_time=.6)
        self.add(ghost)
        self.mark("before")
        self.play(ApplyMatrix([[1, .7], [0, 1]], moving),
                  Transform(vector, Arrow(ORIGIN, [1.7, 1, 0], buff=0, color=GOLD)), run_time=2)
        self.finish()


class BasisToMatrix(PatternScene):
    def construct(self):
        self.intro("Carry meaning into the notation", "The two vector destinations become the two matrix columns.")
        origin = np.array([-3.2, -.5, 0])
        axes = VGroup(Line(origin + LEFT * 1.5, origin + RIGHT * 2.8, color=MUTED),
                      Line(origin + DOWN, origin + UP * 2.8, color=MUTED))
        first = Arrow(origin, origin + [2, 1, 0], color=BLUE, buff=0)
        second = Arrow(origin, origin + [-1, 2, 0], color=TEAL, buff=0)
        first_coords = Matrix([[2], [1]], element_to_mobject=lambda x: math(str(x), BLUE, 27)).scale(.7).move_to([-.45, .65, 0])
        second_coords = Matrix([[-1], [2]], element_to_mobject=lambda x: math(str(x), TEAL, 27)).scale(.7).move_to([-5.25, 1.6, 0])
        target = Matrix([[2, -1], [1, 2]], element_to_mobject=lambda x: math(str(x), size=36)).move_to([3, .2, 0])
        columns = target.get_columns()
        columns[0].set_color(BLUE)
        columns[1].set_color(TEAL)
        self.play(Create(axes), GrowArrow(first), GrowArrow(second), run_time=.8)
        self.play(FadeIn(first_coords), FadeIn(second_coords), FadeIn(target.get_brackets()), run_time=.7)
        self.mark("geometry")
        self.play(TransformFromCopy(first_coords.get_entries(), columns[0]), run_time=.9)
        self.play(TransformFromCopy(second_coords.get_entries(), columns[1]), run_time=.9)
        self.play(FadeIn(math("A =", size=40).next_to(target, LEFT)), run_time=.5)
        self.finish()


class PairwiseGrid(PatternScene):
    def construct(self):
        self.intro("Find the row, the column, the result", "A selected key and query determine one score.")
        keys = np.array([[1, 0], [0, 1], [1, 1]])
        queries = np.array([[1, 2], [2, -1], [-1, 1]])
        scores = keys @ queries.T
        cells = {}
        rows, cols = VGroup(), VGroup()
        for i in range(3):
            y = 1.2 - i * .95
            rows.add(math(rf"\mathbf{{k}}_{i}", BLUE).move_to([-2.7, y, 0]))
            for j in range(3):
                cells[i, j] = math(str(scores[i, j])).move_to([-1.2 + j * 1.5, y, 0]).set_opacity(.2)
        for j in range(3):
            cols.add(math(rf"\mathbf{{q}}_{j}", TEAL).move_to([-1.2 + j * 1.5, 2.05, 0]))
        self.play(FadeIn(rows), FadeIn(cols), *[FadeIn(c) for c in cells.values()], run_time=.8)
        focus = None
        equation = None
        for i, j in [(0, 1), (2, 1), (2, 2)]:
            new_focus = VGroup(SurroundingRectangle(rows[i], color=BLUE, buff=.12),
                               SurroundingRectangle(cols[j], color=TEAL, buff=.12),
                               SurroundingRectangle(cells[i, j], color=GOLD, buff=.18))
            new_eq = math(rf"\mathbf{{k}}_{i}^{{\mathsf T}}\mathbf{{q}}_{j}={scores[i,j]}", GOLD).move_to([4, .1, 0])
            if focus is None:
                self.play(Create(new_focus), run_time=.6)
                self.play(cells[i, j].animate.set_opacity(1), FadeIn(new_eq), run_time=.7)
            else:
                self.play(Transform(focus, new_focus), Transform(equation, new_eq),
                          cells[i, j].animate.set_opacity(1), run_time=.8)
            focus, equation = (new_focus, new_eq) if focus is None else (focus, equation)
            self.mark(f"pair-{i}-{j}")
            self.wait(.5)
        self.play(*[c.animate.set_opacity(1) for c in cells.values()], run_time=.6)
        self.finish()


class NormalizeColumn(PatternScene):
    def construct(self):
        self.intro("Normalize the whole group", "Changing one score changes every probability in this column.")
        scores = np.array([0.0, 1.0, 2.0])
        weights = np.exp(scores - scores.max())
        weights /= weights.sum()
        assert np.isclose(weights.sum(), 1)
        raw = VGroup(*[math(str(int(s)), BLUE).move_to([-3.5, 1.2-i, 0]) for i, s in enumerate(scores)])
        context = VGroup(*[math(str(i), MUTED).move_to([-5, 1.2-i, 0]).set_opacity(.3) for i in range(3)])
        result = VGroup(*[math(f"{w:.3f}", TEAL).move_to([1, 1.2-i, 0]) for i, w in enumerate(weights)])
        arrow = Arrow([-2.5, .2, 0], [-.2, .2, 0], color=GOLD, buff=0)
        self.add(prose("Scores", 25, BLUE).move_to([-3.5, 2.1, 0]),
                 prose("Probabilities", 25, TEAL).move_to([1, 2.1, 0]))
        self.play(FadeIn(raw), FadeIn(context), run_time=.7)
        self.play(Create(SurroundingRectangle(raw, color=GOLD, buff=.25)), run_time=.5)
        self.mark("scores")
        self.play(GrowArrow(arrow), FadeIn(prose("softmax", 25).next_to(arrow, UP)),
                  TransformFromCopy(raw, result), run_time=1.2)
        bars = VGroup(*[Rectangle(width=4*float(w), height=.35, fill_opacity=.7, color=TEAL)
                       .align_to(np.array([2, 1.2-i, 0]), LEFT).set_y(1.2-i) for i, w in enumerate(weights)])
        brace = Brace(result, DOWN, color=GOLD)
        total = math(r"\sum_i p_i=1", GOLD, 31).next_to(brace, DOWN)
        self.play(FadeIn(bars), Create(brace), Write(total), run_time=.8)
        self.finish()


class WeightedAccumulation(PatternScene):
    def construct(self):
        self.intro("Weight first, then accumulate", "A scalar example: source values stay visible while their contributions combine.")
        weights = [.2, .3, .5]
        values = [1, 4, 2]
        contributions = [w*v for w, v in zip(weights, values)]
        terms = VGroup(*[math(rf"{w}\times {v}={c:.1f}", color).move_to([x, 1, 0])
                         for w, v, c, x, color in zip(weights, values, contributions, [-4, 0, 4], [BLUE, TEAL, GOLD])])
        total = DecimalNumber(0, num_decimal_places=1, font_size=48).move_to([.5, -1, 0])
        label = prose("Running sum", 26).next_to(total, LEFT, buff=.6)
        self.play(FadeIn(terms), FadeIn(total), FadeIn(label), run_time=.8)
        self.mark("contributions")
        partial = 0
        for index, contribution in enumerate(contributions):
            traveling = math(f"{contribution:.1f}", [BLUE, TEAL, GOLD][index]).move_to(terms[index])
            self.add(traveling)
            self.play(traveling.animate.move_to(total.get_center() + RIGHT*1.5), run_time=.7)
            partial = sum(contributions[:index+1])
            self.play(total.animate.set_value(partial), FadeOut(traveling), run_time=.5)
        assert np.isclose(partial, 2.4)
        self.play(FadeIn(math(r"\sum_i w_i v_i=2.4", GOLD).move_to([0, -2.2, 0])), run_time=.8)
        self.finish()


class DetailToFormula(PatternScene):
    def construct(self):
        self.intro("Compress a mechanism you already understand", "Keys and queries occupy columns; the compact expression keeps that convention.")
        grid = VGroup(*[math(rf"\mathbf{{k}}_{i}^{{\mathsf T}}\mathbf{{q}}_{j}", BLUE if i == 0 else TEAL, 30)
                       .move_to([-3.7+j*2.1, 1-i*1.7, 0]) for i in range(2) for j in range(2)])
        outline = SurroundingRectangle(grid, color=MUTED, buff=.3)
        symbol = math("S", GOLD, 58).move_to([1.5, .15, 0])
        eq = MathTex("S", "=", r"K^{\mathsf T}", "Q", font_size=52).move_to([4, .15, 0])
        eq[0].set_color(GOLD)
        eq[2].set_color(BLUE)
        eq[3].set_color(TEAL)
        self.play(FadeIn(grid), Create(outline), run_time=.8)
        self.wait(.8)
        self.mark("detail")
        self.play(TransformFromCopy(grid, symbol), run_time=1)
        self.play(ReplacementTransform(symbol, eq[0]), Write(eq[1:]), run_time=1.2)
        self.play(Create(Arrow(outline.get_right(), eq.get_left(), buff=.25, color=GOLD)), run_time=.6)
        self.finish()


class SlidingWindow(PatternScene):
    def construct(self):
        self.intro("Align, compute, then advance", "Full convolution: each output sums exactly the aligned index pairs.")
        a, b = [1, 2, 3], [4, 5]
        spacing, left = 1.7, -3.4
        top = VGroup(*[VGroup(code(str(value), 32, BLUE).move_to([left+i*spacing, 1.1, 0]),
                             code(f"a[{i}]", 18, BLUE).move_to([left+i*spacing, 1.7, 0])) for i, value in enumerate(a)])
        bottom = VGroup(*[VGroup(code(str(value), 32, TEAL).move_to([left+j*spacing, -.05, 0]),
                                code(f"b[{j}]", 18, TEAL).move_to([left+j*spacing, -.6, 0])) for j, value in enumerate(b)])
        labels = VGroup(prose("a", 27, BLUE).move_to([-5.8, 1.1, 0]),
                        prose("b", 27, TEAL).move_to([-5.8, -.05, 0]))
        self.play(FadeIn(top), FadeIn(bottom), FadeIn(labels), run_time=.6)
        # Align b[j] at position n-j: reverse once, then translate one step per output.
        self.play(*[bottom[j].animate.shift(LEFT * (2*j*spacing)) for j in range(len(b))], run_time=.8)
        outputs = VGroup(*[code("?", 27).move_to([-2.55+n*spacing, -2.15, 0]) for n in range(len(a)+len(b)-1)])
        output_labels = VGroup(*[code(f"c[{n}]", 16, MUTED).move_to([-2.55+n*spacing, -1.7, 0]) for n in range(len(outputs))])
        index = code("n = 0", 24, GOLD).move_to([4.3, 1.4, 0])
        self.add(index, math("i+j=n", GOLD, 30).move_to([4.3, .7, 0]), output_labels)
        self.play(FadeIn(outputs), run_time=.4)
        previous_equation = None
        computed = []
        for n in range(len(outputs)):
            if n:
                self.play(FadeOut(previous_equation), run_time=.2)
                self.play(bottom.animate.shift(RIGHT*spacing),
                          Transform(index, code(f"n = {n}", 24, GOLD).move_to(index)), run_time=.6)
            pairs = [(i, n-i) for i in range(len(a)) if 0 <= n-i < len(b)]
            highlights = VGroup(*[SurroundingRectangle(VGroup(top[i], bottom[j]), color=GOLD, buff=.15) for i, j in pairs])
            result = sum(a[i]*b[j] for i, j in pairs)
            computed.append(result)
            formula = "+".join(rf"{a[i]}\cdot {b[j]}" for i,j in pairs) + f"={result}"
            equation = math(formula, GOLD, 30).move_to([1.2, -1.05, 0])
            self.play(Create(highlights), run_time=.4)
            self.play(Write(equation), run_time=.8)
            previous_equation = equation
            self.play(Transform(outputs[n], code(str(result), 27, GOLD).move_to(outputs[n])), run_time=.5)
            self.mark(f"output-{n}")
            self.play(FadeOut(highlights), run_time=.2)
        assert computed == np.convolve(a, b).tolist() == [4, 13, 22, 15]
        self.finish()
