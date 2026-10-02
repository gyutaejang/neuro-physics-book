from figstyle import plt, np, save, C
from matplotlib.patches import Polygon

rng = np.random.default_rng(3)
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.3))


def utube(ax, hl, hr, title):
    # 관 안의 물 (왼쪽 팔, 아래 연결부, 오른쪽 팔)
    water = "#d6e4f2"
    ax.add_patch(plt.Rectangle((0, 0), 3, 0.8, color=water, lw=0))
    ax.add_patch(plt.Rectangle((0, 0.8), 1, hl - 0.8, color=water, lw=0))
    ax.add_patch(plt.Rectangle((2, 0.8), 1, hr - 0.8, color=water, lw=0))
    # 관 벽
    outline = [(0, 4.2), (0, 0), (3, 0), (3, 4.2)]
    ax.plot(*zip(*outline), color=C["ink"], lw=1.4)
    ax.plot([1, 1, 2, 2], [4.2, 0.8, 0.8, 4.2], color=C["ink"], lw=1.4)
    # 반투과막
    ax.plot([1.5, 1.5], [0, 0.8], color=C["gray"], lw=2.2, ls=(0, (2, 1.5)))
    # 용질 입자 (오른쪽에만)
    n = 0
    while n < 26:
        x, y = rng.uniform(1.6, 2.92), rng.uniform(0.08, min(hr, 3.0) - 0.1)
        if y > 0.75 and x < 2.08:
            continue
        ax.scatter([x], [y], s=16, color=C["green"], zorder=3)
        n += 1
    ax.set_title(title, fontsize=10)
    ax.set_xlim(-0.3, 4.3)
    ax.set_ylim(-0.7, 4.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, 4.3, "순수한 물", ha="center", va="bottom", fontsize=8.5, color=C["blue"])
    ax.text(2.5, 4.3, "용액", ha="center", va="bottom", fontsize=8.5, color=C["green"])
    ax.text(1.5, -0.2, "반투과막 (물만 통과)", ha="center", va="top", fontsize=8, color=C["gray"])


utube(axes[0], 2.6, 2.6, "처음: 수면 높이가 같다")
axes[0].annotate("", xy=(1.85, 0.4), xytext=(1.15, 0.4),
                 arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.8, mutation_scale=13))
axes[0].text(1.5, 1.0, "물이\n건너간다", ha="center", va="bottom", fontsize=8, color=C["blue"])

utube(axes[1], 1.8, 3.4, "평형: 용액 쪽 수면이 h만큼 높다")
ax = axes[1]
ax.plot([0.9, 3.25], [1.8, 1.8], color=C["gray"], lw=0.7, ls=":")
ax.plot([2.0, 3.25], [3.4, 3.4], color=C["gray"], lw=0.7, ls=":")
ax.annotate("", xy=(3.2, 3.4), xytext=(3.2, 1.8),
            arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.4))
ax.text(3.32, 2.6, "h", fontsize=11, color=C["red"], va="center")
ax.text(3.3, 1.45, "ρgh = π", fontsize=8.5, color=C["red"], va="top")
fig.tight_layout()
save(fig, __file__)
