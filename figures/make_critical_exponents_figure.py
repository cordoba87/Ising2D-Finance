"""Critical exponents of the S&P 1500 'spin lattice' vs 2D Ising (Onsager) and mean field.

Values from the report, Cuadro 15 (all days) and Cuadro 17 (VIX-filtered days).
Usage: python figures/make_critical_exponents_figure.py  (writes the PNGs next to this script)
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
names = [r"$\nu$", r"$\alpha$", r"$\beta$", r"$\gamma$"]
desc = ["correlation length", "specific heat", "magnetization", "susceptibility"]
all_days = [(0.519, 0.017), (0.932, 0.071), (0.006, 0.004), (1.056, 0.038)]
vix = [(0.526, 0.032), (0.922, 0.105), (0.013, 0.030), (1.052, 0.086)]
onsager = [1.0, 0.0, 0.125, 1.75]
mean_field = [0.5, 0.0, 0.5, 1.0]

themes = {
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#59636e", grid="#d1d9e0", s1="#2a78d6", s2="#eb6834"),
    "dark": dict(bg="#0d1117", fg="#e6edf3", muted="#9198a1", grid="#3d444d", s1="#3987e5", s2="#d95926"),
}

for name, t in themes.items():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11, "mathtext.fontset": "dejavusans",
        "text.color": t["fg"], "axes.labelcolor": t["fg"], "xtick.color": t["muted"], "ytick.color": t["fg"],
        "axes.edgecolor": t["grid"], "figure.facecolor": t["bg"], "axes.facecolor": t["bg"],
    })
    fig, ax = plt.subplots(figsize=(10, 4.7))
    y = np.arange(len(names))[::-1].astype(float)
    for yi in y:
        ax.axhline(yi, color=t["grid"], lw=0.6, zorder=0)
    ax.scatter(onsager, y, marker="D", s=90, facecolors="none", edgecolors=t["fg"], linewidths=1.6,
               zorder=4, label="2D Ising exact (Onsager)")
    ax.scatter(mean_field, y, marker="X", s=80, color=t["muted"], linewidths=0, zorder=3,
               label="Mean field")
    for (vals, col, dy, lab) in [(all_days, t["s1"], 0.17, "Market, all days"),
                                 (vix, t["s2"], -0.17, "Market, VIX 70–95th pct. days")]:
        v = np.array(vals)
        ax.errorbar(v[:, 0], y + dy, xerr=v[:, 1], fmt="o", ms=8, color=col, ecolor=col, elinewidth=1.8,
                    capsize=0, mec=t["bg"], mew=1.5, zorder=5, label=lab)
    ax.set_yticks(y, [f"{n}  {d}" for n, d in zip(names, desc)])
    ax.set_ylim(-0.6, len(names) - 0.4)
    ax.set_xlim(-0.12, 1.9)
    ax.set_xlabel("critical exponent value")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0, pad=8)
    ax.grid(axis="x", color=t["grid"], lw=0.6, alpha=0.6)
    ax.set_title("S&P 1500 (2017–2018) as a 2D spin lattice\nν and γ sit near mean field; α and β match neither model",
                 loc="left", fontsize=12, pad=12)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.17), ncol=4, frameon=False, fontsize=9.5,
              handletextpad=0.4, columnspacing=1.4)
    fig.tight_layout()
    fig.savefig(f"{out_dir}/critical_exponents_{name}.png", dpi=150, facecolor=t["bg"])
    plt.close(fig)
print("ok")
