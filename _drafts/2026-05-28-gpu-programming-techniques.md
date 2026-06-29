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
throughput is hard: a naive kernel (a GPU program) often lands at *single-digit percentages* of
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


## The Roofline Model

The roofline model tells you a kernel's performance *upper bound* on a given machine —
and, more importantly, why it's capped: by memory or by compute. Real kernels almost always land
below it.

The two axes:
- X-axis: arithmetic intensity — FLOP (floating-point operations: add, multiply, …)
  per byte of data moved from DRAM. A measure of data reuse: how many operations
  each byte feeds before it's thrown away.
- Y-axis: attainable performance, in FLOP/s (floating-point operations per second).

Every benchmark in this post runs on one GPU — an NVIDIA RTX 5070 Ti —
and the picture below is its roofline. The numbers behind it:

| Spec | RTX 5070 Ti |
|---|---|
| Peak compute (FP32 = 32-bit float) | 44 TFLOP/s (8960 [FP32 lanes](#sm) × 2.45 GHz × 2 for FMA) |
| Memory bandwidth | 896 GB/s (GDDR7, 256-bit) |
| Architecture | Blackwell GB203, 70 [SMs](#sm), 16 GB |

![NVIDIA RTX 5070 Ti FP32 roofline — the 896 GB/s memory diagonal meets the 44 TFLOP/s compute roof at the ridge (≈ 49 FLOP/byte); the naive matmul sits at AI ≈ 0.25, far down the diagonal.](/assets/images/rtx5070ti-roofline.png)

*RTX 5070 Ti FP32 roofline, drawn on log–log axes — every gridline a 10× step, which is
what turns the memory ceiling into a straight diagonal.*

In one line: `attainable performance = min(peak compute, bandwidth × AI)` — the lower
ceiling wins. The flat top is peak compute: every ALU issuing a fused multiply-add
every cycle, and no arithmetic intensity, however high, beats it. The diagonal is the
memory ceiling, `bandwidth × AI`: at low intensity even saturating memory leaves the
ALUs starved — work arrives slower than they can consume it — so performance climbs
only as AI rises, until it meets the flat top. Where they cross is the ridge:
`peak FLOP/s ÷ peak bandwidth = 44 TFLOP/s ÷ 896 GB/s ≈ 49 FLOP/byte` on the
RTX 5070 Ti — the least reuse a kernel needs to reach peak compute. (Both 49 and the
0.25 below are FP32 figures — 4 bytes per element; lower precision packs more numbers
per byte and runs on faster units, sliding both the point and the ridge right.)

Where a kernel falls on the x-axis tells you which fix to reach for. Left of the ridge
it's memory-bound, and the lever is reuse: raise arithmetic intensity and climb the
diagonal. Right of it, compute-bound — more reuse buys nothing; you need more FLOP/s
(better ILP, the tensor cores, or fewer FLOPs). Naive matmul lands at AI ≈ 0.25, ~200×
left of the ridge, against the bandwidth roof. The rest of this post walks it right.


# GPU and CUDA basics
- Before we dive into kernels, its important to have some background. Your CPU has maybe 8
or 16 cores, and each one is very complex: deep caches, branch prediction ... - a hudge 
transistor budget spent making a single thread finish as fast as possible. A GPU has a 
different design philosophy. It spends that same budget on thousands of simple cores and 
accepts that each one, alone, is *slow*. A CPU is a handful of elite generals; a GPU is a 
massive army of basic soldiers.

For most code, the elite generals win. But when you have the same operation to run across a
a million data elements - add two vectors, multiple two matrices - the army wins, and it's not close.

*The mental shift*, in one example. On a CPU you add two arrays with a loop: 



# Matrix Multiplications

### The climb

<!-- per rung: technique → what it does → benchmark (% peak + roofline point).
     bottleneck implicit, numbers = [[placeholder]]. -->

#### 1. Naive (uncoalesced)
- technique: one thread per output `C[i][j]`; loop k, read a row of A + a column of B from global memory.
- does: no reuse — A read N times, B read N times; AI ≈ 0.25. Scattered loads waste each transaction.
- benchmark: [[% peak]] — sits *below* the diagonal. (first benchmark → one-line L2→DRAM cliff aside: small N hides in L2; all sizes here are past the spill.)

#### 2. Coalesced   [TODO — small kernel, reindex threads]
- technique: map threads so a warp's 32 loads hit contiguous addresses.
- does: same math, same AI — climbs *up* onto the bandwidth roof. The free lunch.
- benchmark: [[% peak]] — on the diagonal now, still left of ridge.

#### 3. Shared-memory tiling
- technique: each block loads a tile of A and B into shared memory once, reuses across its threads.
- does: cuts DRAM traffic → AI rises → walk *right* toward the ridge. Still memory-bound.
- benchmark: [[% peak]] — further right on the diagonal.

#### 4. Register tiling   [TODO]
- technique: each thread computes several outputs, operands in registers (1D → 2D).
- does: AI rises again — and the obvious move (crank occupancy) BACKFIRES: more registers/thread → fewer warps (less TLP) but more independent work/thread (more ILP), net faster. ← conceptual peak.
- benchmark: [[% peak]], [[achieved occupancy]] — crossing toward compute-bound.

#### 5. Vectorized loads / float4   [TODO]
- technique: wider loads (`float4`), fewer load instructions.
- does: removes the last memory-side stall → lands compute-bound.
- benchmark: [[% peak]] — right of the ridge.

#### Landing — the gap to cuBLAS
- compute-bound now, still [[X]]% under cuBLAS. why: tensor cores, hand-tuned PTX, async copy.
- the loop that transfers: profile → which bound? → fix → re-measure.
- tensor cores (FP16/FP4) = next frontier, named not benchmarked.


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
