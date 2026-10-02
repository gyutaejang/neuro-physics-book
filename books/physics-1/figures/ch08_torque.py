from figstyle import plt, np, save, C
from matplotlib.patches import FancyArrowPatch, Ellipse, Arc

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw=dict(width_ratios=[1, 1.3]))

# (가) 자기장 속 전류 고리와 자기 모멘트
for y in np.linspace(-1.2, 1.2, 5):
    ax1.add_patch(FancyArrowPatch((-1.8, y), (1.8, y), arrowstyle="-|>", mutation_scale=10,
                                  color=C["purple"], lw=0.8, alpha=0.55))
th = np.deg2rad(50)
ux, uy = np.cos(th), np.sin(th)
# 고리를 비스듬히 본 타원 (법선이 μ 방향)
ax1.add_patch(Ellipse((0, 0), 1.3, 0.45, angle=np.rad2deg(th) + 90, fill=False, lw=2.0, color=C["blue"], zorder=4))
ax1.add_patch(FancyArrowPatch((0, 0), (1.25 * ux, 1.25 * uy), arrowstyle="-|>", mutation_scale=14,
                              color=C["red"], lw=2.0, zorder=5))
ax1.text(1.3 * ux + 0.05, 1.3 * uy, "μ (자기 모멘트)", color=C["red"], fontsize=9, va="bottom",
         bbox=dict(fc="white", ec="none", pad=1), zorder=6)
ax1.add_patch(Arc((0, 0), 1.2, 1.2, theta1=0, theta2=50, color=C["ink"], lw=0.9))
ax1.text(0.68, 0.25, "θ", fontsize=10)
ax1.text(1.85, -1.45, "B", color=C["purple"], fontsize=10, ha="right")
ax1.text(0, -1.75, "토크가 μ를 B 쪽으로 돌린다", ha="center", fontsize=8.5)
ax1.set_xlim(-1.9, 1.9)
ax1.set_ylim(-1.9, 1.7)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("(가) 자기장 속의 전류 고리", fontsize=10.5)

# (나) 토크와 에너지
deg = np.linspace(0, 180, 181)
t = np.deg2rad(deg)
ax2.plot(deg, -np.cos(t), color=C["blue"], label="에너지 U = −μB cos θ")
ax2.plot(deg, np.sin(t), color=C["red"], ls="--", label="토크 크기 τ = μB sin θ")
ax2.axhline(0, color=C["gray"], lw=0.6)
ax2.plot([0], [-1], "o", color=C["blue"], ms=5)
ax2.plot([180], [1], "o", mfc="white", color=C["blue"], ms=5)
ax2.text(6, -1.12, "안정: μ가 B와 같은 방향", fontsize=8.5, va="top")
ax2.text(176, 1.12, "불안정: 반대 방향", fontsize=8.5, ha="right", va="bottom")
ax2.set_xticks([0, 45, 90, 135, 180])
ax2.set_xlim(0, 180)
ax2.set_ylim(-1.45, 1.45)
ax2.set_yticks([-1, 0, 1])
ax2.set_yticklabels(["−μB", "0", "+μB"])
ax2.set_xlabel("μ와 B 사이 각 θ (도)")
ax2.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.1))
ax2.set_title("(나) 각도에 따른 에너지와 토크", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
