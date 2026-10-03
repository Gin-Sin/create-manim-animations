# Animation patterns from 3Blue1Brown references

This is a practical catalog, not a claim to reproduce an author's exact production process. The **reference observation** in each entry describes evidence from a named lesson. The **recipe**, durations, example code, and interactive adaptation are original recommendations for new explanations. See [source notes](3b1b-source-notes.md) for timestamp provenance and which visuals were inspected.

The executable examples are original Manim Community scenes in [assets/pattern_gallery.py](../assets/pattern_gallery.py). They use CMU Serif prose, JetBrains Mono code, and LaTeX math. They are silent staging studies; add shared-script narration using the existing timing guide rather than reading their titles as a separate voice script.

## Select a pattern by explanatory need

| Need | Pattern | Runnable scene |
| --- | --- | --- |
| Explain a repeated operation | P01 · one item, then all items | `OneThenMany` |
| Reduce visual clutter without losing identity | P02 · arrows to points | `ArrowsToPoints` |
| Show what changed relative to a baseline | P03 · fixed reference, moving data | `ReferenceGrid` |
| Connect geometric meaning to notation | P04 · destinations to matrix columns | `BasisToMatrix` |
| Explain a pairwise computation | P05 · select row, column, and cell | `PairwiseGrid` |
| Explain a normalization invariant | P06 · isolate, normalize, restore context | `NormalizeColumn` |
| Explain a reduction | P07 · weight before accumulating | `WeightedAccumulation` |
| Summarize an understood mechanism | P08 · details into compact notation | `DetailToFormula` |
| Explain a repeated local computation | P09 · align, compute, step | `SlidingWindow` |

Choose only patterns that make the model clearer. Several may compose: use P01 to teach one computation, P05/P06 to explain its table, then P08 to summarize it. Do not make every operation an elaborate morph.

Timing values below are seconds for new scenes, not measurements from the videos. They cover visual beats, not the full duration of narration. Extend the useful hold using measured speech; let slower speech finish without globally slowing down every motion.

## P01 · Explain one item, then expand to the collection

**Reference:** [Attention, 06:42–07:13](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=402s), A1. The lesson shows a single embedding/query relationship before displaying the corresponding query computation for the token sequence.

**Use when:** a batch applies the same operation to many items, but the viewer needs one complete causal example first.

**Stage:** keep inputs aligned and outputs in a second lane. De-emphasize other inputs, reveal one connecting operation and its result, pause, then restore the other inputs and reveal equivalent operations with a small stagger.

**Timing recipe:** establish 0.5; first operation 1.1; explanation hold 0.7 or speech duration; fan-out 1.4 with `lag_ratio` around 0.15–0.25; final hold 0.8.

**Implementation:** `OneThenMany` uses `FadeIn`, `GrowArrow`, and `LaggedStart`. Do not copy the numerical output of the first item to every item; repeat the operation while computing each output separately.

**Interactive adaptation:** a selected token determines the detailed lane. “Show all” reveals the same mapping for every token without changing model values. Block conflicting input while lanes move; reduced motion jumps to the same selection/context state.

**PagedAttention use:** follow one token's logical block and offset before adding the other tokens' mappings.

**Failure to avoid:** showing every arrow, label, and formula at once; viewers cannot tell which object caused which result.

## P02 · Simplify the representation while preserving the object

**Reference:** [Linear transformations, 01:16–02:06](https://www.youtube.com/watch?v=kYB8IZa5AuE&t=76s), L1. Dense origin-based arrows become easier to follow as endpoint dots and then as a field of positions. Official companion clips confirm the representations and movement.

**Use when:** a faithful depiction becomes too crowded at scale.

**Stage:** show a small arrow collection, emphasize one arrow, identify its endpoint, then replace each arrow with a dot at that exact endpoint. Keep the selected item's color/identity through the simplification. Only after that should the field transform.

**Timing recipe:** establish 0.6; selected-item emphasis 0.6; arrow-to-dot change 1.0; transform field 1.6; settle 0.8.

**Implementation:** `ArrowsToPoints` pairs each arrow with its endpoint dot using `ReplacementTransform`. Store semantic IDs separately from either representation. Do not teleport dots to a newly sorted order.

**Interactive adaptation:** an “arrows / points” toggle preserves selection and coordinates. A transform slider changes the underlying positions regardless of representation; rebuilding the view must not reset the selected item.

**PagedAttention use:** replace detailed K/V vector components with compact token cells after introducing what the cells stand for. Make the abstraction explicit before reducing detail.

**Failure to avoid:** deleting identifying labels/color at the same time as changing both scale and position; the simplified mark loses its referent.

## P03 · Keep a fixed reference while the data moves

**Reference:** [Linear transformations, 02:06–02:13](https://www.youtube.com/watch?v=kYB8IZa5AuE&t=126s), L2. A subdued original grid remains behind the transformed grid, preserving a coordinate reference.

**Use when:** viewers must compare before/after positions, shape, allocation, or capacity.

**Stage:** draw the reference faintly, duplicate only the transformable geometry, introduce a selected vector, and transform the foreground. Maintain the camera and reference origin unless the explanation specifically needs a camera move.

**Timing recipe:** reference 0.5; foreground 0.6; transform 1.8–2.5; comparison hold 1.0.

**Implementation:** `ReferenceGrid` uses separate `NumberPlane` objects and applies `ApplyMatrix` only to the foreground. Keep selected arrows out of the background group. A vector's new endpoint must equal the same matrix applied to its original coordinates.

**Interactive adaptation:** expose transform amount or matrix entries. Recompute targets from immutable original coordinates; do not repeatedly transform an already transformed position on each slider event. Reduced motion shows the final transform plus the baseline.

**PagedAttention use:** keep logical token order fixed while physical-block assignments change. Unlike a geometric transform, remapping need not move the underlying data; label the operation accurately.

**Failure to avoid:** moving camera, reference, and foreground together so nothing remains to explain the displacement.

## P04 · Carry geometric identity into symbolic notation

**Reference:** [Linear transformations, 06:04–06:53](https://www.youtube.com/watch?v=kYB8IZa5AuE&t=364s), L3. The destinations of the two basis vectors provide the two matrix columns.

**Use when:** a formula or table is a compact description of something already visible.

**Stage:** show destination vectors in distinct semantic colors; reveal their coordinates nearby; create an empty or faint matrix; copy the corresponding coordinate values into each column while maintaining color and order. Retain the geometric source long enough to compare.

**Timing recipe:** geometry 0.8; coordinate labels 0.7; first correspondence 0.9; second 0.9; comparison hold 1.0.

**Implementation:** `BasisToMatrix` uses `Matrix.get_columns()` and explicit source-to-target `TransformFromCopy` pairings. This is a copy of a representation, not a second mutation of the model. Avoid string-wide morphs that swap matching repeated digits between columns.

**Interactive adaptation:** editing a matrix column updates the matching vector and vice versa. Keep a single numerical state for both views and validate the coordinate convention.

**PagedAttention use:** carry a colored logical block into its block-table row and corresponding physical page, with explicit IDs instead of unexplained floating labels.

**Failure to avoid:** treating color as decoration, or transposing row/column conventions midway through the correspondence.

## P05 · Resolve a pairwise relationship at a grid intersection

**Reference:** [Attention, 08:27–09:29](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=507s), A2. Query/key relationships are organized as a grid with visual emphasis on stronger matches.

**Use when:** a result depends on one item from each of two collections.

**Stage:** establish row and column labels; select one row and one column; move both guides to their intersection; reveal that pair's computation and value. Repeat a few examples before displaying the whole grid. Use magnitude marks only with an explicit encoding; raw negative scores cannot be encoded as negative dot radii.

**Timing recipe:** labels/grid 0.8; guides 0.6; result 0.7; read hold 0.5; next pair 0.6–0.9.

**Implementation:** `PairwiseGrid` computes `keys @ queries.T` and uses `SurroundingRectangle` for row/column/cell focus. Numeric contents come from the model, not random decorative values.

**Interactive adaptation:** selecting a row or column updates its highlighted intersection, equation, and accessible result. Keep keyboard alternatives to pointer-based cell selection. The highlighted result must update atomically with both indices.

**PagedAttention use:** relate a query to keys gathered from different physical pages; grid indexing remains logical, even if retrieval order differs.

**Failure to avoid:** confusing screen row order with physical memory order or inferring attention probabilities from unnormalized raw scores.

## P06 · Isolate a group, normalize it, then restore context

**Reference:** [Attention, 09:29–10:10](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=569s), A3. A column is singled out for softmax and then returned to the larger normalized attention grid.

**Use when:** the operation has an invariant shared across a group, such as a sum of one or a conserved total.

**Stage:** dim unrelated groups without deleting their context; show the complete selected score column; transform scores to probabilities; add a brace and total; restore the other columns only after the denominator is clear.

**Timing recipe:** focus 0.5; normalization 1.0–1.4; invariant 0.8; comparison hold 1.0; context return 0.6.

**Implementation:** `NormalizeColumn` computes a numerically stable softmax by subtracting the maximum score first. It displays the probability column, bar magnitudes, and the full-column sum. Rounded display values may differ slightly from the exact total; validate unrounded values and explain rounding when visible.

**Interactive adaptation:** a score slider recomputes all probabilities for that selected group together. Keep the sum visible. Do not interpolate independently computed columns that imply a different normalization axis.

**PagedAttention use:** emphasize that valid keys from all physical pages contribute to one normalization for the query, rather than normalizing independently inside each page.

**Failure to avoid:** splitting one denominator into per-page groups for visual convenience.

## P07 · Weight each contribution before accumulating

**Reference:** [Attention, 14:42–15:50](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=882s), A5. Values are scaled by the chosen column's weights and combined into an update.

**Use when:** a reduction or mixture needs to expose what contributes and by how much.

**Stage:** display source values and weights separately; reveal scaled contributions; connect those contributions to the destination one at a time; update a running total; finally show the compact sum. Keep original values visible while copies move.

**Timing recipe:** sources 0.7; weight application 0.8–1.1; each contribution 0.5–0.8; final sum 0.8; read hold 1.0.

**Implementation:** `WeightedAccumulation` uses a small exact example, explicit contribution values, traveling copies, and a model-derived running total. Its scalar values are a stated simplification of a vector reduction. `TransformFromCopy` illustrates contribution flow without destroying the source.

**Interactive adaptation:** a “step contribution” button advances a prefix index. Recompute the sum from that prefix so reset/replay cannot double-add a value. Sliders can change weights only after revalidating any required sum constraint.

**PagedAttention use:** demonstrate value-vector reduction after globally normalized weights. Clarify whether the animation illustrates the mathematics or the actual kernel's reduction order.

**Failure to avoid:** moving the original source away, suggesting it was consumed or removed from the cache.

## P08 · Compress an explained mechanism into notation

**Reference:** [Attention, 10:18–11:01](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=618s), A4. The explicit query/key grid is related to a compact matrix expression.

**Use when:** the viewer has followed a concrete computation and now needs a reusable abstraction.

**Stage:** preserve the detailed working view; reveal one symbolic result; connect detail to the corresponding symbol; then assemble or highlight the compact expression. Keep a small overview or labels so zooming out does not erase meaning.

**Timing recipe:** detailed view hold 0.8; correspondence 1.0; compact expression 1.0–1.4; compare 1.2.

**Implementation:** `DetailToFormula` maps entries of a score matrix to `S`, then adds `S = K^T Q` with dimensions/conventions stated. Use explicit correspondence when repeated symbols make automatic `TransformMatchingTex` ambiguous. Morph only when it communicates identity; an explanatory arrow can be clearer.

**Interactive adaptation:** a detail/overview toggle preserves the same numerical model and selection. When a user edits a score-producing input, update the underlying detailed computation before refreshing the summary.

**PagedAttention use:** connect one worked `t → block → offset → physical slot` example to the general address rule. Only introduce compact notation after its components have referents.

**Failure to avoid:** displaying the final formula first and treating subsequent movement as decoration.

## P09 · Align a window, compute, then advance

**Reference:** [Convolution, 06:31–07:08](https://www.youtube.com/watch?v=KuXjwB4LzSA&t=391s), C1. The timed example shifts a reversed sequence through successive alignments and forms outputs from aligned products. This entry is supported by captions/source, rather than a full-video playback review.

**Use when:** repeated local work produces a sequence of outputs, including scans, filters, tiles, or block-boundary operations.

**Stage:** display both index spaces; explicitly reverse the sequence if the mathematical operation requires it; move to one alignment; highlight only overlapping pairs; show their products and sum; write one output; advance exactly one index.

**Timing recipe:** orient/reverse 0.8; slide 0.6; paired emphasis 0.4; computation 0.8; output 0.5; repeat. The first example may take longer than subsequent ones.

**Implementation:** `SlidingWindow` computes full discrete convolution from explicit index pairs. The lower row is reversed once and then translated; output `n` includes only pairs with `i + j = n`. Its separate output slots retain their final values.

**Interactive adaptation:** a step index selects alignment and output; “next” is a state transition, not a timer-only visual. A scrubber can inspect completed outputs without mutating their mathematical values. Preserve the distinction between convolution and cross-correlation.

**PagedAttention use:** step a token index through a fixed-size block; show a different event when the offset wraps to zero. Do not imply that paging itself reverses tokens or performs convolution.

**Failure to avoid:** sliding or wrapping graphics without updating the indices that define which items participate.

## Run and review the gallery

From a project with Manim Community, LaTeX, and the specified fonts:

```bash
python -m manim -ql --fps 30 /path/to/create-manim-animations/assets/pattern_gallery.py \
  OneThenMany ArrowsToPoints ReferenceGrid BasisToMatrix PairwiseGrid \
  NormalizeColumn WeightedAccumulation DetailToFormula SlidingWindow
```

Use the examples as staging components, not as finished narrated lessons. Review a beginning, active-motion, and final frame for each adapted scene. Verify numeric invariants independently: mapping identity, transformed coordinates, dot products, softmax total, weighted sum, and convolution indices. For browser adaptations, additionally test selection persistence, conflicting controls, reduced motion, and intermediate frames using the [interactive guide](interactive-animation.md).
