from figstyle import plt, np, save, C
from matplotlib.patches import Circle, FancyArrowPatch

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), gridspec_kw=dict(width_ratios=[1, 1.35]))

# (가) 도선을 위에서 본 그림: 전류는 종이에서 나오는 방향
for r in (0.45, 0.85, 1.25):
    ax1.add_patch(Circle((0, 0), r, fill=False, color=C["purple"], lw=1.0))
    for ang in (45, 165, 285):
        t = np.deg2rad(ang)
        p0 = (r * np.cos(t), r * np.sin(t))
        d = (-np.sin(t) * 0.01, np.cos(t) * 0.01)
        ax1.add_patch(FancyArrowPatch(p0, (p0[0] + d[0], p0[1] + d[1]),
                                      arrowstyle="-|>", mutation_scale=11, color=C["purple"]))
ax1.add_patch(Circle((0, 0), 0.13, color=C["red"], zorder=3))
ax1.add_patch(Circle((0, 0), 0.04, color="white", zorder=4))
ax1.text(0, -1.5, "전류 I: 종이에서 나오는 방향(⊙)\n자기장: 시계 반대 방향 원", ha="center", va="top", fontsize=8.5)
ax1.set_xlim(-1.6, 1.6)
ax1.set_ylim(-2.1, 1.5)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("(가) 직선 도선 둘레의 자기장", fontsize=10.5)

# (나) B = μ0 I / (2π r)
mu0 = 4e-7 * np.pi
r = np.linspace(0.005, 0.20, 300)
for I, col, lab in ((1, C["blue"], "I = 1 A"), (10, C["red"], "I = 10 A")):
    ax2.plot(r * 100, mu0 * I / (2 * np.pi * r) * 1e6, color=col, label=lab)
ax2.axhline(50, color=C["gray"], ls="--", lw=0.9)
ax2.text(19.8, 53, "지구 자기장 약 50 μT", ha="right", va="bottom", fontsize=8.5, color=C["gray"])
ax2.set_xlabel("도선에서 떨어진 거리 r (cm)")
ax2.set_ylabel("자기장 B (μT)")
ax2.set_ylim(0, 200)
ax2.set_xlim(0, 20)
ax2.legend(loc="upper right", fontsize=8.5)
ax2.set_title(r"(나) 거리에 반비례: $B = \mu_0 I / 2\pi r$", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
