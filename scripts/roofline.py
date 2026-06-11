#!/usr/bin/env python3
"""Roofline plot for the "GPU Bottlenecks" post (RTX 5070 Ti, Blackwell GB203).

CUDA-core (FP32) focused: FP32 is the hero roofline. Tensor-core ceilings are
drawn faint, for context only -- "the next frontier" the post names.

Regenerate:
    python3 scripts/roofline.py
Outputs assets/images/rtx5070ti-roofline.{png,svg}.

The blog locks clocks with `nvidia-smi -lgc`, so the *sustained* clock can be
below the marketing boost. To redraw the flat compute roof at a locked clock,
change BOOST_CLOCK_GHZ below -- the FP32 peak is derived from
cores x clock x 2 (FMA) in-code, never hardcoded.
"""

import matplotlib

matplotlib.use("Agg")  # headless: write files, no display needed
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# Hardware parameters -- RTX 5070 Ti (Blackwell GB203). Edit these to retarget.
# Sources: TechPowerUp gpu-specs, NVIDIA RTX 5070 family page (June 2026).
# ----------------------------------------------------------------------------
CUDA_CORES = 8960          # shading units
BOOST_CLOCK_GHZ = 2.452    # reference boost. Set to your locked clock for honest % of peak.
FLOPS_PER_FMA = 2          # FMA = multiply + add = 2 FLOP
MEM_BW_GBPS = 896.0        # GDDR7, 256-bit bus, 28 Gbps/pin

# FP32 (CUDA-core) compute peak, DERIVED -- not hardcoded.
FP32_PEAK_TFLOPS = CUDA_CORES * BOOST_CLOCK_GHZ * FLOPS_PER_FMA / 1000.0  # ~44 TFLOP/s

# Tensor-core ceilings (5th-gen), for context. Dense / 2:4-sparse, TFLOP/s.
# FP16/BF16: 88 / 176 | FP8: 176 / 352 | FP4: 494 / 988 (988 ~ "1406 AI TOPS" class).
# We draw ONE tensor roof (FP16/BF16 dense) to stay uncluttered; others noted here.
TENSOR_FP16_DENSE_TFLOPS = 87.9
TENSOR_FP4_SPARSE_TFLOPS = 988.0  # drawn faintest, labels the FP4 "next frontier"

# Operating point the draft cites: naive matmul, ~200x left of the ridge.
NAIVE_MATMUL_AI = 0.25  # FLOP/byte

# ----------------------------------------------------------------------------
# Roofline geometry
# ----------------------------------------------------------------------------
def ridge_ai(peak_tflops, bw_gbps):
    """Arithmetic intensity (FLOP/byte) where the bandwidth roof meets the
    flat compute roof: peak FLOP/s / peak bytes/s."""
    return (peak_tflops * 1e12) / (bw_gbps * 1e9)


def attainable_tflops(ai, peak_tflops, bw_gbps):
    """min(compute roof, memory roof) at a given arithmetic intensity."""
    mem_roof = (bw_gbps * 1e9) * ai / 1e12  # BW * AI, in TFLOP/s
    return np.minimum(peak_tflops, mem_roof)


fp32_ridge = ridge_ai(FP32_PEAK_TFLOPS, MEM_BW_GBPS)

# ----------------------------------------------------------------------------
# Plot
# ----------------------------------------------------------------------------
plt.rcParams.update(
    {
        "font.size": 12,
        "axes.titlesize": 15,
        "axes.labelsize": 12,
        "legend.fontsize": 10,
        "figure.dpi": 110,
    }
)

fig, ax = plt.subplots(figsize=(8.2, 5.6))

ai = np.logspace(-2, 3.2, 600)  # 0.01 .. ~1585 FLOP/byte

# --- FP32 hero roofline (memory diagonal + compute flat top) ---
ax.plot(ai, attainable_tflops(ai, FP32_PEAK_TFLOPS, MEM_BW_GBPS),
        color="#1f4e79", lw=2.6, zorder=5, label="FP32 attainable roof")

# --- Faint tensor-core ceilings, context only ---
ax.axhline(TENSOR_FP16_DENSE_TFLOPS, color="#7a7a7a", lw=1.3, ls="--",
           alpha=0.6, zorder=2)
ax.axhline(TENSOR_FP4_SPARSE_TFLOPS, color="#b0b0b0", lw=1.2, ls=":",
           alpha=0.55, zorder=2)

# --- FP32 flat compute roof emphasis + label ---
ax.axhline(FP32_PEAK_TFLOPS, color="#1f4e79", lw=1.4, ls="-", alpha=0.35, zorder=3)

# --- Ridge point ---
ax.plot([fp32_ridge], [FP32_PEAK_TFLOPS], "o", color="#1f4e79",
        ms=8, zorder=6)
ax.annotate(
    f"ridge ~ {fp32_ridge:.0f} FLOP/byte\n(FP32 peak / BW)",
    xy=(fp32_ridge, FP32_PEAK_TFLOPS),
    xytext=(fp32_ridge * 1.5, FP32_PEAK_TFLOPS * 0.34),
    fontsize=10, color="#1f4e79",
    arrowprops=dict(arrowstyle="->", color="#1f4e79", lw=1.2),
)

# --- Naive matmul operating point (on the bandwidth diagonal) ---
naive_perf = attainable_tflops(np.array([NAIVE_MATMUL_AI]), FP32_PEAK_TFLOPS, MEM_BW_GBPS)[0]
ax.plot([NAIVE_MATMUL_AI], [naive_perf], "D", color="#c0392b", ms=8, zorder=7)
ax.annotate(
    f"naive matmul\nAI ~ {NAIVE_MATMUL_AI} (~{fp32_ridge / NAIVE_MATMUL_AI:.0f}x left of ridge)",
    xy=(NAIVE_MATMUL_AI, naive_perf),
    xytext=(NAIVE_MATMUL_AI * 1.4, naive_perf * 7),
    fontsize=10, color="#c0392b",
    arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.2),
)

# --- Roof text labels (placed on the lines) ---
# (memory-roof label is added after layout, below, so its angle can be
#  computed from the final display transform.)
ax.text(620, FP32_PEAK_TFLOPS * 1.07,
        f"FP32 compute roof\n{FP32_PEAK_TFLOPS:.0f} TFLOP/s "
        f"({CUDA_CORES} x {BOOST_CLOCK_GHZ:g} GHz x 2)",
        color="#1f4e79", fontsize=10, va="bottom", ha="right")
ax.text(620, TENSOR_FP16_DENSE_TFLOPS * 1.05, "FP16/BF16 tensor (dense)",
        color="#5a5a5a", fontsize=9, va="bottom", ha="right")
ax.text(620, TENSOR_FP4_SPARSE_TFLOPS * 1.04, "FP4 tensor (sparse) -- the next frontier",
        color="#888888", fontsize=9, va="bottom", ha="right")

# --- Axes cosmetics ---
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.01, 1585)
ax.set_ylim(0.05, 1600)  # low enough to show the naive-matmul point at ~0.22 TFLOP/s
ax.set_xlabel("Arithmetic intensity (FLOP / byte)")
ax.set_ylabel("Attainable performance (TFLOP/s)")
ax.set_title("RTX 5070 Ti roofline (FP32)")
ax.grid(True, which="both", ls=":", lw=0.5, color="#cccccc", alpha=0.8)
ax.set_axisbelow(True)

fig.tight_layout()

# Memory-roof label, placed along the visible diagonal. Its angle is computed
# from the actual display transform after layout, so it stays glued to the line
# even if the limits or figure size change (a hardcoded angle does not).
fig.canvas.draw()
_ai0 = 1.0
_y0 = MEM_BW_GBPS * 1e9 * _ai0 / 1e12
_p0 = ax.transData.transform((_ai0, _y0))
_p1 = ax.transData.transform((_ai0 * 10, MEM_BW_GBPS * 1e9 * _ai0 * 10 / 1e12))
_angle = float(np.degrees(np.arctan2(_p1[1] - _p0[1], _p1[0] - _p0[0])))
ax.text(_ai0, _y0 * 1.3, f"memory roof — {MEM_BW_GBPS:.0f} GB/s",
        rotation=_angle, rotation_mode="anchor",
        color="#1f4e79", fontsize=10, va="bottom", ha="left")

# ----------------------------------------------------------------------------
# Export
# ----------------------------------------------------------------------------
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "images")
os.makedirs(OUT_DIR, exist_ok=True)
png = os.path.join(OUT_DIR, "rtx5070ti-roofline.png")
svg = os.path.join(OUT_DIR, "rtx5070ti-roofline.svg")
fig.savefig(png, dpi=170, bbox_inches="tight")
fig.savefig(svg, bbox_inches="tight")
print(f"FP32 peak  = {FP32_PEAK_TFLOPS:.2f} TFLOP/s")
print(f"ridge AI   = {fp32_ridge:.1f} FLOP/byte")
print(f"wrote {png}")
print(f"wrote {svg}")
