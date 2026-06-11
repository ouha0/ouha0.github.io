---
title: "GPU Bottlenecks"
date: 2026-05-28
categories:
  - notes
tags:
  - gpu
  - cuda
  - performance
---

## Introduction

GPUs should be fast — that's the point. But getting one to run near its rated
throughput is hard: a naive kernel often lands at *single-digit percentages* of
what the hardware is capable of.

Compute has outpaced memory bandwidth for decades, so a chip's arithmetic units
(ALUs) crunch numbers far faster than memory can feed them. The bottleneck is
moving data, not doing math. A CPU hides the latency with caches, branch
prediction, and out-of-order execution. A GPU hides it with parallelism: when one
warp (32 threads run in lockstep) stalls on memory, the hardware switches to
another that's ready.

We'll use a single example throughout — matrix multiplication — and walk it up a
ladder of optimization techniques, benchmarking each step to see which bottleneck
it resolves and what the next one becomes. Matmul is simple to state, yet each
value loaded from memory feeds many multiplies — so the same data can be reused
instead of re-fetched. How much of that reuse you capture decides whether memory
or compute limits you, and a single kernel travels all the way from memory-bound
to compute-bound.

*GPU-specific terms (warp, SM, occupancy, coalescing, …) are defined in the
[glossary](#glossary) at the end - refer back as you read.*


## The Roofline

The roofline model tells you a kernel's performance *upper bound* on a given machine —
and, more importantly, why it's capped: by memory or by compute. Real kernels almost always land
below it.

The two axes:
- X-axis: arithmetic intensity — FLOP (floating-point operations: add, multiply, …)
  per byte of data moved from DRAM. A measure of data reuse: how many operations
  each byte feeds before it's thrown away.
- Y-axis: attainable performance, in FLOP/s (floating-point operations per second).

Every benchmark in this post runs on one card — an RTX 5070 Ti (Blackwell GB203) —
and the picture below is its roofline. The numbers behind it:

| Spec | RTX 5070 Ti |
|---|---|
| Peak compute (FP32 = 32-bit float) | 44 TFLOP/s (8960 [FP32 lanes](#sm) × 2.45 GHz × 2 for FMA) |
| Memory bandwidth | 896 GB/s (GDDR7, 256-bit) |
| Architecture | Blackwell GB203, 70 [SMs](#sm), 16 GB |

(have the roofline picture here)

In one line: `attainable = min(peak compute, bandwidth × AI)` — whichever ceiling is
lower wins. The flat top is peak compute — `lanes × clock × 2` for the fused
multiply-add — and no arithmetic intensity, however high, beats it. The diagonal is
the memory ceiling, `bandwidth × AI`: at low intensity even saturating memory leaves
the ALUs starved, and performance climbs only as AI rises, until it meets the flat
top. Where the two cross is the ridge — `peak FLOP/s ÷ peak bandwidth`, or
`44 TFLOP/s ÷ 896 GB/s ≈ 49 FLOP/byte` on the RTX 5070 Ti: the least reuse a kernel
needs to reach peak compute. (Both 49 and the 0.25 below are FP32 figures — 4 bytes
per element; lower precision like FP4 packs more numbers per byte and runs on faster
units, sliding both the point and the ridge.)

Where a kernel falls along the x-axis tells you which fix to reach for. Left of 49
it is memory-bound, and the only lever is reuse: raise arithmetic intensity and you
climb the diagonal. Right of 49 it is compute-bound, and more reuse buys nothing —
you need faster math. The naive matmul lands at AI ≈ 0.25, about 200× left of the ridge
and pinned to the bandwidth ceiling. The rest of this post is improving that.


## Kernel case studies

*How to read the numbers below:* clocks are locked, every result is a percentage of
the card's peak rather than a raw speedup, and the baseline is cuBLAS (NVIDIA's
hand-tuned library — the bar to beat), not my own naive kernel. Full rig and
one-command reproduction are in the appendix.

One measurement trap is worth seeing first. The roofline above is drawn against
*DRAM* bandwidth — but at small sizes a kernel's data fits in L2 cache, giving it
reuse the DRAM roofline never counted. It effectively sits right of where that
roofline places it and looks faster than it is — you're timing the cache, not the
896 GB/s DRAM. Push the size up and throughput falls off a cliff as the working set
spills to DRAM:

*(L2 → DRAM cliff plot)*

Every benchmark here is taken past that cliff, at sizes large enough to saturate all
70 SMs.

<!-- Per-kernel template — every kernel follows the same 5-beat shape: -->
- (a) Intuitive description of the technique
- (b) The kernel (approach / code)
- (c) Benchmark — size sweep, % of peak, point on the roofline
- (d) **Intuitive bottleneck close — 4 beats:**
  1. What's starving (binding resource, one sentence)
  2. The one number that proves it (a profiler metric, not a vibe)
  3. The physical picture (analogy)
  4. Why the next fix targets exactly that
  > Discipline: every intuition anchored to one measured number.
- (e) Bridge to the next kernel

### SGEMM — the ridge-crossing arc (the spine)
- Technique arc: naive → shared-memory tiling → register tiling (1D → 2D) →
  vectorized loads (float4).
- Narrative spine: **arithmetic intensity climbs across 49; the bottleneck FLIPS
  from memory to compute.** Naive ≈ 0.25 FLOP/byte (~200× left of ridge).
- **Deep-idea callout at the register-tiling step — occupancy vs ILP is a tradeoff,
  not a goal:** more registers/thread → fewer resident warps (less TLP) but more
  independent work (more ILP). Show the version where pushing occupancy *hurts*.
  (This backfire is the "what didn't work" centerpiece — keep it here, on the
  critical path, not quarantined later.)
- Anchor metrics: arithmetic intensity, % of FP32 peak, achieved occupancy.
- Baseline: the cuBLAS gap (honest scoreboard).
- Size: N ≥ 4096 (each matrix ~67 MB); sweep 1024 → 8192.

### Reduction — memory-bound (the coda)
- Short, ~2 beats: proves the same diagnostic loop finds a kernel that *stays* left
  of the ridge — the method transfers even when the bottleneck doesn't move.
- Technique arc: naive → coalesced → warp-shuffle (`__shfl`).
- Anchor metrics: DRAM throughput %, sectors per request.
- Analogy: full truck sent to fetch one box (uncoalesced). Tops out *on the slope*
  at ~bandwidth peak — and that's correct, not a failure.
- Size: hundreds of MB – 1 GB.

<!-- Histogram (contention-bound) CUT — a third bottleneck class deflates the
     memory→compute arc after the ridge-crossing climax. Candidate for a follow-up. -->


## What didn't work
- The occupancy-hurts backfire now lives on the SGEMM critical path (register-tiling
  step above) — don't repeat it here.
- The speedup that didn't materialize.
- Register spills (too much shared memory / too many registers → occupancy drop).
- The cuBLAS gap I couldn't close, and why: tensor-core paths, hand-tuned PTX,
  async copy I didn't implement.


## Closing — where it stops, what transfers
- cuBLAS / CUTLASS exist; the point was understanding, not shipping a GEMM. Tensor
  cores (5th-gen, FP4) are the next frontier — named, not benchmarked in this
  CUDA-core post.
- Kernel tuning is **hardware-specific**: the best tile sizes, register-blocking
  factors, and occupancy targets depend on *this* card's SM / register / shared-memory
  budget, and the ridge itself is per-card. It's why cuBLAS autotunes and ships
  hundreds of variants — a kernel hand-tuned for one GPU rarely stays optimal on the
  next. Near-peak performance takes a lot of tuning.
- The loop that transfers, stated once: **profile → which bound? → fix → re-measure.**
  Tiling, coalescing, privatization are just the moves; the loop is the method.
  (Show one concrete transfer — e.g. attention — or cut the claim.)


---

## Appendix — GPU vocabulary for CPU people {#glossary}

*The GPU-specific terms used in the post are defined here; CPU analogies in
parentheses. Skim it, or refer back as you read.*

**Throughput vs. latency** — latency is how long one operation takes; throughput
is how many finish per second. CPUs optimize latency, GPUs optimize throughput.

**FLOP** — one floating-point operation (an add or a multiply). "FLOPs"
(lowercase, a *count*) is not "FLOPS" (a *rate*, per second).

**FLOP/s, TFLOP/s** — floating-point ops per second; the chip's math throughput.
Tera = 10¹². The 5070 Ti does ~44 TFLOP/s in FP32.

**FMA (fused multiply-add)** — `a*b + c` as one instruction. Counts as 2 FLOPs —
that's the ×2 in every peak-FLOP formula. The workhorse of matmul.

**Memory bandwidth** — bytes per second moved between DRAM and the chip (GB/s).
The 5070 Ti: ~896 GB/s.

**Arithmetic intensity (AI)** — FLOPs done per byte read from DRAM (FLOP/byte).
The one number that says whether a kernel is starved for math or for data.

**Memory-bound** — runtime limited by bandwidth; the ALUs sit idle waiting on
data. Low AI. Fix: move less, reuse more.

**Compute-bound** — runtime limited by the ALUs; the memory system has slack.
High AI. Fix: do less math, or use faster units (e.g. tensor cores).

**Roofline / ridge point** — plot achievable FLOP/s against AI: a sloped
bandwidth ceiling meeting a flat compute ceiling. The corner — the *ridge*, at
peak-FLOP/s ÷ peak-bandwidth ≈ 49 FLOP/byte here — is the AI where a kernel
flips from memory-bound (left) to compute-bound (right).

**SIMT** — the GPU runs one program across many threads at once.

**Warp** — 32 threads issued together in lockstep. The real unit of execution
and scheduling.

<a id="sm"></a>
**SM (streaming multiprocessor)** — the GPU's actual "core": its own schedulers,
register file, and L1/shared memory. The 5070 Ti has 70, each 128 lanes wide —
so think "70 wide cores," not "9000." (A "CUDA core" is just one ALU lane inside
an SM, *not* a core.)

**Occupancy** — how many warps are resident on an SM vs. the max. It's the GPU's
supply of ready work it can switch to while other warps wait on memory.

**Global memory** — off-chip DRAM; big and slow (≈ system RAM).

**Shared memory** — a small on-chip scratchpad, explicitly managed, shared
within a block (≈ a software-controlled L1).

**Coalescing** — when a warp's 32 threads touch contiguous addresses, the
hardware fuses them into one wide transaction; scattered addresses waste most of
each fetch (≈ cache-line utilization).


## Appendix — rig and reproduction

- **Card:** RTX 5070 Ti (Blackwell GB203), 70 SMs, 16 GB GDDR7. Compiled
  `-arch=sm_120`, CUDA 12.8+ (`deviceQuery` to confirm).
- **Clocks locked** with `nvidia-smi -lgc`; peak is derived from that *sustained*
  clock, not the marketing boost. (The 44 TFLOP/s in the spec table is the 2.45 GHz
  boost figure — if you lock lower, recompute the flat roof at the locked clock so
  "% of peak" stays honest.)
- **Timing:** CUDA events, warmup, N iterations; reported as median + spread, never
  a single run.
- **Metric of record:** % of the card's peak (bandwidth or FLOP/s), not raw speedup.
- **Baseline:** cuBLAS / CUB, not just my own naive kernel.
- **Reproduction:** pinned repo — one command regenerates every number and plot.


## Notes to self (not post body)
- Full rig: driver + CUDA versions, exact clock settings, `deviceQuery` dump; confirm L2 size.
- References (cite + differentiate against):
  - siboehm.com/articles/22/CUDA-MMM — gold-standard SGEMM worklog; I differ by
    leading with *diagnosis*, not the sequence.
  - salykova.github.io/sgemm-gpu — expert PTX/async.
  - abhik.ai — memory-centric interactive viz.
  - answer.ai WebGPU Puzzles — concept-first.
- My edge: profiler-driven diagnosis + rigorous methodology (locked clocks,
  % of peak, size sweeps past L2, real baselines). Don't drift into another
  trick-list worklog.
