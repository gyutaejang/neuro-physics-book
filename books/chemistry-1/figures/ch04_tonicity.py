from figstyle import plt, np, save, C
from matplotlib.patches import Circle, FancyBboxPatch

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(width_ratios=[1.5, 1]))

cases = [
    ("고장액\n(예: 350 mOsm)", 0.62, "out"),
    ("등장액\n(약 290 mOsm)", 0.80, None),
    ("저장액\n(예: 200 mOsm)", 0.9, "in"),
]
for i, (lab, r, flow) in enumerate(cases):
    cx = i * 2.6
    a1.add_patch(FancyBboxPatch((cx - 1.15, -1.15), 2.3, 2.3, boxstyle="round,pad=0.02",
                                fc=C["light"], ec=C["gray"], lw=0.8))
    a1.add_patch(Circle((cx, 0), r, fc="#dcebd8", ec=C["green"], lw=1.6))
    a1.text(cx, -1.35, lab, ha="center", va="top", fontsize=8.5)
    if flow:
        for ang in np.deg2rad([30, 150, 270]):
            ux, uy = np.cos(ang), np.sin(ang)
            r_in, r_out = (r - 0.32, r + 0.2) if flow == "out" else (r - 0.34, r + 0.22)
            a, b = (r_in, r_out) if flow == "out" else (r_out, r_in)
            a1.annotate("", xy=(cx + b * ux, b * uy), xytext=(cx + a * ux, a * uy),
                        arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.4, mutation_scale=10))
a1.text(0, 1.3, "물이 빠져 쪼그라든다", ha="center", fontsize=8, color=C["blue"])
a1.text(2.6, 1.3, "알짜 이동 없음", ha="center", fontsize=8, color=C["gray"])
a1.text(5.2, 1.3, "물이 들어와 붓는다", ha="center", fontsize=8, color=C["blue"])
a1.set_xlim(-1.3, 6.5)
a1.set_ylim(-2.2, 1.6)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 바깥 삼투 농도와 세포 부피 (반트호프-보일 관계)
pi = np.linspace(180, 400, 200)
ideal = 290 / pi
b = 0.3
real = b + (1 - b) * 290 / pi
a2.plot(pi, ideal, color=C["green"], lw=2, label="완전한 삼투계")
a2.plot(pi, real, color=C["green"], lw=1.2, ls="--", label="삼투 비활성 부피 30%")
a2.axhline(1, color=C["gray"], lw=0.6, ls=":")
a2.axvline(290, color=C["gray"], lw=0.6, ls=":")
a2.scatter([290], [1], color=C["ink"], s=18, zorder=3)
a2.set_xlabel("바깥 삼투 농도 (mOsm/L)")
a2.set_ylabel("세포 부피 (등장액 = 1)")
a2.set_xlim(180, 400)
a2.set_ylim(0.65, 1.65)
a2.legend(fontsize=7.5, loc="upper right")
fig.tight_layout()
save(fig, __file__)
