from figstyle import plt, np, save, C

# 크뤼거-글로버 모형: tSNR = SNR0 / sqrt(1 + lam^2 SNR0^2)
s0 = np.logspace(np.log10(3), 3, 400)
fig, ax = plt.subplots(figsize=(6.0, 3.1))
lam = 0.01
t = s0 / np.sqrt(1 + (lam * s0) ** 2)
ax.plot(s0, s0, color=C["gray"], lw=0.8, ls="--")
ax.axhline(1 / lam, color=C["gray"], lw=0.8, ls="--")
ax.plot(s0, t, color=C["blue"], lw=2)
ax.text(52, 80, "열 잡음만 있을 때\ntSNR = SNR₀", fontsize=8, color=C["gray"], ha="right")
ax.text(560, 104, "생리 잡음의 천장 1/λ = 100", fontsize=8, color=C["gray"], ha="center")
pts = [(200, "3 T, 3 mm"), (200 * 8 / 27, "3 T, 2 mm"), (200 * 1 / 27, "3 T, 1 mm"),
       (200 * 8 / 27 * 2.3, "7 T, 2 mm")]
for v, name in pts:
    tv = v / np.sqrt(1 + (lam * v) ** 2)
    col = C["red"] if name.startswith("7") else C["blue"]
    ax.plot(v, tv, "o", color=col, ms=5, zorder=3)
    dx, dy, ha = {"3 T, 3 mm": (1.12, -14, "left"), "3 T, 2 mm": (0.85, 4, "right"),
                  "3 T, 1 mm": (0.85, 7, "right"), "7 T, 2 mm": (1.0, -24, "center")}[name]
    ax.text(v * dx, tv + dy, f"{name}\ntSNR {tv:.0f}", fontsize=8, color=col, ha=ha)
ax.set_xscale("log")
ax.set_xlim(3, 1000)
ax.set_ylim(0, 125)
ax.set_xlabel("영상 한 장의 SNR₀ (열 잡음 기준)")
ax.set_ylabel("시계열 tSNR")
fig.tight_layout()
save(fig, __file__)
