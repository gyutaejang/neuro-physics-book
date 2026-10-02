from figstyle import plt, np, save, C
from matplotlib.patches import Polygon, Circle, Ellipse

G = C["green"]
rng = np.random.default_rng(11)
fig, axes = plt.subplots(1, 4, figsize=(7.4, 3.4), gridspec_kw=dict(width_ratios=[1.1, 1, 1.25, 0.8]))


def branch(ax, x, y, ang, length, depth, lw, spread=0.45, shrink=0.7, color=G):
    x2, y2 = x + length * np.cos(ang), y + length * np.sin(ang)
    ax.plot([x, x2], [y, y2], color=color, lw=lw, solid_capstyle="round")
    if depth > 0:
        for d in (-spread, spread):
            branch(ax, x2, y2, ang + d + rng.normal(0, 0.12), length * shrink, depth - 1, lw * 0.75, spread, shrink, color)


def axon(ax, x, y, length):
    ax.plot([x, x], [y, y - length], color=C["red"], lw=1.0)


# (가) 피라미드 뉴런
ax = axes[0]
ax.add_patch(Polygon([(0, 0.35), (-0.25, -0.15), (0.25, -0.15)], fc="#dcebd8", ec=G, lw=1.3, zorder=3))
ax.plot([0, 0], [0.35, 2.5], color=G, lw=2.2)
for a in (np.pi / 2 - 0.5, np.pi / 2, np.pi / 2 + 0.5):
    branch(ax, 0, 2.5, a, 0.35, 2, 1.2)
for yb, a in [(1.2, 0.5), (1.6, np.pi - 0.5), (0.8, np.pi - 0.6)]:
    branch(ax, 0, yb, a, 0.35, 1, 1.0)
for a in (-0.4, -1.0, -2.1, -2.7):
    branch(ax, 0.2 * np.cos(a), -0.15, a, 0.35, 2, 1.1)
axon(ax, 0, -0.15, 1.3)
ax.text(0.08, -1.35, "축삭", color=C["red"], fontsize=7.5)
ax.set_title("(가) 피라미드 뉴런", fontsize=9)
ax.text(0, -1.85, "피질 2/3·5·6층, 해마\n흥분성 (글루탐산)", ha="center", va="top", fontsize=7.6)

# (나) 가시 성상 뉴런
ax = axes[1]
ax.add_patch(Circle((0, 0.5), 0.17, fc="#dcebd8", ec=G, lw=1.3, zorder=3))
for a in np.linspace(0, 2 * np.pi, 8, endpoint=False) + 0.2:
    branch(ax, 0.17 * np.cos(a), 0.5 + 0.17 * np.sin(a), a, 0.38, 2, 1.1, spread=0.4)
axon(ax, 0, 0.33, 1.6)
ax.text(0.08, -1.1, "축삭", color=C["red"], fontsize=7.5)
ax.set_title("(나) 가시 성상 뉴런", fontsize=9)
ax.text(0, -1.85, "피질 4층 (특히 1차 감각 피질)\n흥분성 (글루탐산)", ha="center", va="top", fontsize=7.6)

# (다) 퍼킨예 세포: 한 평면에 펼쳐진 부채꼴 수상돌기
ax = axes[2]
ax.add_patch(Ellipse((0, 0), 0.4, 0.5, fc="#dcebd8", ec=G, lw=1.3, zorder=3))
ax.plot([0, 0], [0.25, 0.65], color=G, lw=2.2)
for a in np.linspace(np.pi / 2 - 1.0, np.pi / 2 + 1.0, 4):
    branch(ax, 0, 0.65, a, 0.45, 4, 1.4, spread=0.32, shrink=0.78)
axon(ax, 0, -0.25, 1.15)
ax.text(0.08, -1.25, "축삭", color=C["red"], fontsize=7.5)
ax.set_title("(다) 퍼킨예 세포", fontsize=9)
ax.text(0, -1.85, "소뇌 피질의 유일한 출력\n억제성 (GABA)", ha="center", va="top", fontsize=7.6)

# (라) 소뇌 과립세포: 아주 작다
ax = axes[3]
ax.add_patch(Circle((0, 0.4), 0.07, fc="#dcebd8", ec=G, lw=1.1, zorder=3))
for a in (0.4, 1.9, 3.5, 5.0):
    x2, y2 = 0.3 * np.cos(a), 0.4 + 0.3 * np.sin(a)
    ax.plot([0.07 * np.cos(a), x2], [0.4 + 0.07 * np.sin(a), y2], color=G, lw=0.9)
    for d in (-0.6, 0, 0.6):
        ax.plot([x2, x2 + 0.06 * np.cos(a + d)], [y2, y2 + 0.06 * np.sin(a + d)], color=G, lw=0.7)
ax.plot([0, 0], [0.47, 2.3], color=C["red"], lw=0.9)
ax.plot([-0.75, 0.75], [2.3, 2.3], color=C["red"], lw=0.9)
ax.text(0, 2.38, "평행 섬유", ha="center", va="bottom", fontsize=7.5, color=C["red"])
ax.set_title("(라) 소뇌 과립세포", fontsize=9)
ax.text(0, -1.85, "세포체 약 5–8 μm\n뇌 뉴런의 절반 이상", ha="center", va="top", fontsize=7.6)

for ax in axes:
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-2.5, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")
axes[2].set_xlim(-1.6, 1.6)
axes[3].set_xlim(-0.95, 0.95)
fig.tight_layout(w_pad=0.3)
save(fig, __file__)
