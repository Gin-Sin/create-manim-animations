# Reference evidence and timestamp notes

This catalog studies three named 3Blue1Brown lessons. It uses short, original observations and new implementation recipes, without redistributing their footage or copying their scene code.

## What was verified

- **Linear transformations:** sampled the official six-second `TransformVectors`, `ManyPointsTransformation`, and `TransformGrid` animation clips at 0.5, 3, and 5.5 seconds; also inspected the official basis-vector clip. These are lesson animations; their local times are **not** timestamps in the full YouTube upload.
- **Attention:** inspected the official lesson's `W_Q`, `Q_I`, `DotProduct`, `SoftMax`, `Normalized`, `Paper`, `Compact`, `DeltaE`, and `MultiHeaded` frames and the author's animation source. Still frames establish composition; source establishes staged operations. Full-video playback was unavailable in the research environment, so the catalog does not claim frame-accurate viewing of that upload.
- **Convolutions:** used the author's timed captions and scene source to locate the sliding-array example. This is a transcript/source-supported example; no full-video motion review is claimed.

Full-video intervals below are located using the author's English sentence timings, rounded outward to whole seconds. They are review windows for the relevant explanation, not exact edit boundaries or measurements of individual animations. The catalog's recommended durations are original starting points for new work.

## Videos and verified review windows

| ID | Video / official lesson | Full-video review window | Catalog patterns |
| --- | --- | --- | --- |
| L1 | [Linear transformations and matrices](https://www.youtube.com/watch?v=kYB8IZa5AuE&t=76s) · [lesson](https://www.3blue1brown.com/lessons/linear-transformations/) | 01:16–02:06 | P02: arrows → points → field |
| L2 | [Same video](https://www.youtube.com/watch?v=kYB8IZa5AuE&t=126s) | 02:06–02:13 | P03: retain a reference grid |
| L3 | [Same video](https://www.youtube.com/watch?v=kYB8IZa5AuE&t=364s) | 06:04–06:53 | P04: geometric destinations → matrix columns |
| A1 | [Attention in transformers, step-by-step](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=402s) · [lesson](https://www.3blue1brown.com/lessons/attention/) | 06:42–07:13 | P01: one operation → all items |
| A2 | [Same video](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=507s) | 08:27–09:29 | P05: pairwise relationships → grid |
| A3 | [Same video](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=569s) | 09:29–10:10 | P06: normalize an emphasized column |
| A4 | [Same video](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=618s) | 10:18–11:01 | P08: expanded computation ↔ compact notation |
| A5 | [Same video](https://www.youtube.com/watch?v=eMlx5fFNoYc&t=882s) | 14:42–15:50 | P07: weight, then accumulate |
| C1 | [But what is a convolution?](https://www.youtube.com/watch?v=KuXjwB4LzSA&t=391s) · [lesson](https://www.3blue1brown.com/lessons/convolutions/) | 06:31–07:08 | P09: shift, align, multiply, sum |

The conventions in the attention lesson use keys/queries as columns and normalize score columns. Other sources often use row vectors and row normalization. Preserve the selected convention across diagrams, matrix dimensions, and equations; never transpose a formula only to resemble a reference screenshot.

## Primary sources

Timing provenance, pinned to the inspected caption repository revision:

- [Linear-transformation timings](https://github.com/3b1b/captions/blob/9aef876b0ed62ce4f099c0a2f0e7a52e8d1058c9/2016/linear-transformations/english/sentence_timings.json)
- [Attention timings](https://github.com/3b1b/captions/blob/9aef876b0ed62ce4f099c0a2f0e7a52e8d1058c9/2024/attention/english/sentence_timings.json)
- [Convolution timings](https://github.com/3b1b/captions/blob/9aef876b0ed62ce4f099c0a2f0e7a52e8d1058c9/2022/convolutions/english/sentence_timings.json)

Author scene source, pinned separately:

- [AttentionPatterns and related scenes](https://github.com/3b1b/videos/blob/306a1346a356c7a7b097875ceb51c5cd67d0a56c/_2024/transformers/attention.py): inspect single-query expansion, `ndp_columns`, `softmax_cols`, `weighted_sum_cols`, and camera-frame changes. This uses the author's ManimGL environment, not the bundled gallery's Community API.
- [Discrete convolutions](https://github.com/3b1b/videos/blob/306a1346a356c7a7b097875ceb51c5cd67d0a56c/_2022/convolutions/discrete.py): inspect array alignment, pairwise products, and output accumulation.

Direct official lesson clips for visual inspection:

- [TransformVectors.mp4](https://storage.googleapis.com/3blue1brown-website-bucket/lessons/2016/linear-transformations/figures/transformations-are-functions/TransformVectors.mp4)
- [ManyPointsTransformation.mp4](https://storage.googleapis.com/3blue1brown-website-bucket/lessons/2016/linear-transformations/figures/transformations-are-functions/ManyPointsTransformation.mp4)
- [TransformGrid.mp4](https://storage.googleapis.com/3blue1brown-website-bucket/lessons/2016/linear-transformations/figures/transformations-are-functions/TransformGrid.mp4)
- [RecordWhereBasisVectorsLand.mp4](https://storage.googleapis.com/3blue1brown-website-bucket/lessons/2016/linear-transformations/figures/matrices/RecordWhereBasisVectorsLand.mp4)

To extend the catalog, retain this distinction: record the video and time window, inspect available visuals/source, write a brief observation, then separately design the new scene's timing and implementation. Do not convert a transcript timestamp into a claimed frame-accurate animation measurement.
