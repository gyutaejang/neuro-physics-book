from figstyle import plt, np, save, C
from matplotlib.patches import FancyArrowPatch, Arc

fig = plt.figure(figsize=(7.4, 2.9))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.45])
ax1, ax2, ax3 = [fig.add_subplot(gs[0, i]) for i in range(3)]


def axes_cross(ax, L=1.35, above=False):
    ax.add_patch(FancyArrowPatch((-L, 0), (L, 0), arrowstyle="-|>", mutation_scale=9, color=C["gray"], lw=0.8))
    ax.add_patch(FancyArrowPatch((0, -L), (0, L), arrowstyle="-|>", mutation_scale=9, color=C["gray"], lw=0.8))
    ax.text(L, 0.07 if above else -0.1, "실수부", ha="right", va="bottom" if above else "top", fontsize=8, color=C["gray"])
    ax.text(0.06, L, "허수부", ha="left", va="top", fontsize=8, color=C["gray"])
    ax.set_xlim(-L - 0.05, L + 0.1)
    ax.set_ylim(-L - 0.05, L + 0.1)
    ax.set_aspect("equal")
    ax.axis("off")


# (가) 복소수 하나 = 평면 위의 화살표
axes_cross(ax1, above=True)
a, b = 0.72, 0.6
r, ph = np.hypot(a, b), np.arctan2(b, a)
ax1.add_patch(FancyArrowPatch((0, 0), (a, b), arrowstyle="-|>", mutation_scale=13, color=C["red"], lw=2, zorder=4))
ax1.plot([a, a], [0, b], color=C["blue"], ls="--", lw=1)
ax1.plot([0, a], [b, b], color=C["blue"], ls="--", lw=1)
ax1.text(a, -0.08, "a", ha="center", va="top", fontsize=10, color=C["blue"])
ax1.text(-0.08, b, "b", ha="right", va="center", fontsize=10, color=C["blue"])
ax1.add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=np.rad2deg(ph), lw=1))
ax1.text(0.34, 0.1, "φ", fontsize=10)
ax1.text(0.26, 0.34, "|z|", fontsize=10, color=C["red"], ha="right")
ax1.text(0, -1.5, "z = a + ib\n크기 |z|, 위상 φ", ha="center", va="top", fontsize=8.8)
ax1.set_ylim(-1.95, 1.45)
ax1.set_title("(가) 복소수는 화살표다", fontsize=10.5)

# (나) e^{iωt}: 단위원 위를 도는 화살표
axes_cross(ax2)
u = np.linspace(0, 2 * np.pi, 200)
ax2.plot(np.cos(u), np.sin(u), color=C["gray"], lw=0.8)
for k, p in enumerate(np.deg2rad([0, 45, 90, 135])):
    ax2.add_patch(FancyArrowPatch((0, 0), (np.cos(p), np.sin(p)), arrowstyle="-|>", mutation_scale=10,
                                  color=C["purple"], lw=1.4, alpha=0.35 + 0.2 * k, zorder=3))
ax2.add_patch(Arc((0, 0), 1.6, 1.6, theta1=10, theta2=125, lw=1.2, color=C["ink"]))
ax2.add_patch(FancyArrowPatch((np.cos(np.deg2rad(122)) * 0.8, np.sin(np.deg2rad(122)) * 0.8),
                              (np.cos(np.deg2rad(128)) * 0.8, np.sin(np.deg2rad(128)) * 0.8),
                              arrowstyle="-|>", mutation_scale=9, color=C["ink"], lw=0))
ax2.text(0, -1.5, "$e^{i\\omega t} = \\cos\\omega t + i\\,\\sin\\omega t$\n각속도 ω로 도는 길이 1의 화살표",
         ha="center", va="top", fontsize=8.8)
ax2.set_ylim(-1.95, 1.45)
ax2.set_title("(나) 회전하는 화살표", fontsize=10.5)

# (다) 그 그림자: 실수부와 허수부
t = np.linspace(0, 2, 400)
ax3.plot(t, np.cos(2 * np.pi * t), color=C["blue"], lw=2, label="실수부 cos ωt")
ax3.plot(t, np.sin(2 * np.pi * t), color=C["red"], lw=2, ls="--", label="허수부 sin ωt")
ax3.axhline(0, color=C["gray"], lw=0.6)
ax3.annotate("", xy=(0.25, 1.12), xytext=(0, 1.12),
             arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8, shrinkA=0, shrinkB=0))
ax3.text(0.125, 1.17, "1/4 주기 (90°)", ha="center", va="bottom", fontsize=8)
ax3.set_xlim(0, 2)
ax3.set_ylim(-1.2, 1.95)
ax3.set_yticks([-1, 0, 1])
ax3.set_xlabel("시간 (주기 단위)")
ax3.legend(loc="upper right", fontsize=7.8, ncol=2, bbox_to_anchor=(1.0, 1.03))
ax3.set_title("(다) 화살표의 두 그림자", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
