from figstyle import plt, save, C

# (값 eV, 이름, 글자 높이). 1–5 eV 부근이 붐비므로 높이를 손으로 정한다.
items = [  # (값 eV, 이름, 글자 높이, 글자 가로 위치)
    (5.3e-7, "3 T MRI RF 광자\n~5×10⁻⁷ eV", 0.75, 5.3e-7),
    (1.0e-5, "전자레인지\n~10⁻⁵ eV", -0.75, 1.0e-5),
    (0.027, "열에너지 kT\n0.027 eV", 0.75, 0.006),
    (0.5, "ATP 분자 하나\n~0.5 eV", -0.75, 0.12),
    (1.55, "근적외선 800 nm\n1.55 eV", 1.45, 0.3),
    (2.6, "청색광 470 nm\n2.6 eV", 0.75, 7),
    (4.5, "자외선 275 nm\n~4.5 eV", -1.45, 7),
    (7e4, "CT X선\n수십 keV", 0.75, 7e4),
    (5.11e5, "PET 감마선\n511 keV", -0.75, 5.11e5),
]
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.set_xscale("log")
ax.set_xlim(1e-7, 5e6)
ax.set_ylim(-2.2, 2.55)
ax.axhline(0, color=C["gray"], lw=1.2, zorder=1)
ax.axvspan(10, 5e6, color=C["red"], alpha=0.08, lw=0)
ax.axvline(10, color=C["red"], lw=1, ls="--")
ax.text(14, 2.5, "전리 방사선 → (약 10 eV 이상)", color=C["red"], fontsize=8.5, va="top")
ax.text(7, 2.5, "← 비전리", color=C["gray"], fontsize=8.5, va="top", ha="right")
for v, name, lvl, tx in items:
    ax.plot([v, tx], [0, lvl * 0.9], color=C["gray"], lw=0.6, zorder=1)
    ax.scatter([v], [0], s=28, color=C["blue"], zorder=3)
    ax.text(tx, lvl, name, ha="right" if tx == 7 else "center", va="bottom" if lvl > 0 else "top", fontsize=8.5, color=C["ink"])
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -2.2))
ticks = [(1e-6, "10⁻⁶"), (1e-4, "10⁻⁴"), (1e-2, "10⁻²"), (1, "1"), (1e2, "10²"), (1e4, "10⁴"), (1e6, "10⁶")]
ax.set_xticks([t for t, _ in ticks])
ax.set_xticklabels([s for _, s in ticks])
ax.minorticks_off()
ax.set_xlabel("광자 하나의 에너지 (eV, 로그 눈금)")
save(fig, __file__)
