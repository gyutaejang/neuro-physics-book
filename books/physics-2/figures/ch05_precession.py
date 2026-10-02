from figstyle import plt, np, save, C
from matplotlib.patches import FancyArrowPatch, Ellipse

fig = plt.figure(figsize=(7.2, 3.3))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# (가) 도는 전하 고리: 각운동량 L과 자기 모멘트 μ가 같은 축 위에 있다
ax1.add_patch(Ellipse((0, 0), 2.2, 0.7, fill=False, lw=2.2, color=C["blue"]))
for ang, sgn in [(-80, 1), (100, -1)]:
    t = np.deg2rad(ang)
    x, y = 1.1 * np.cos(t), 0.35 * np.sin(t)
    ax1.add_patch(FancyArrowPatch((x - 0.25 * sgn, y), (x + 0.25 * sgn, y), arrowstyle="-|>",
                                  mutation_scale=13, color=C["blue"], lw=0))
ax1.text(1.25, -0.42, "+ 전하가 돈다", fontsize=8.5, color=C["blue"])
ax1.add_patch(FancyArrowPatch((0, 0), (0, 1.45), arrowstyle="-|>", mutation_scale=14,
                              color=C["ink"], lw=2))
ax1.add_patch(FancyArrowPatch((0.12, 0), (0.12, 1.05), arrowstyle="-|>", mutation_scale=14,
                              color=C["purple"], lw=2))
ax1.text(-0.12, 1.5, "각운동량 L", ha="right", fontsize=9, color=C["ink"])
ax1.text(0.25, 0.95, "자기 모멘트 μ = γL", fontsize=9, color=C["purple"])
ax1.text(0, -1.05, "μ와 L은 늘 같은 축 위에 있다\n비례 상수 γ = 자기회전비", ha="center", fontsize=8.5)
ax1.set_xlim(-1.7, 2.1)
ax1.set_ylim(-1.45, 1.8)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("(가) 도는 전하는 자석이자 팽이다", fontsize=10.5)

# (나) 세차: 토크 μ × B가 μ를 옆으로 민다 (원근을 손으로 그린 도식)
from matplotlib.patches import Arc
cx, cz, a, b = 0.0, 1.3, 0.75, 0.22   # 끝이 그리는 원(타원으로 보임)
ax2.add_patch(Ellipse((cx, cz), 2 * a, 2 * b, fill=False, lw=1.0, ls="--", color=C["gray"]))
for p in np.linspace(0, 2 * np.pi, 13)[:-1]:
    ax2.plot([0, a * np.cos(p)], [0, cz + b * np.sin(p)], color=C["gray"], lw=0.4, alpha=0.5)
ax2.add_patch(FancyArrowPatch((0, 0), (0, 1.95), arrowstyle="-|>", mutation_scale=14,
                              color=C["purple"], lw=1.8))
ax2.text(0.06, 1.92, "B₀", color=C["purple"], fontsize=10.5)
p0 = np.deg2rad(-35)
mx, mz = a * np.cos(p0), cz + b * np.sin(p0)
ax2.add_patch(FancyArrowPatch((0, 0), (mx, mz), arrowstyle="-|>", mutation_scale=15,
                              color=C["red"], lw=2.2, zorder=5))
ax2.text(mx + 0.06, mz - 0.18, "μ", color=C["red"], fontsize=11)
# 토크 방향: 타원의 접선(종이 앞쪽으로 돌아 나오는 방향)
tx, tz = -a * np.sin(p0), b * np.cos(p0)
n = np.hypot(tx, tz)
ax2.add_patch(FancyArrowPatch((mx, mz), (mx + 0.45 * tx / n, mz + 0.45 * tz / n), arrowstyle="-|>",
                              mutation_scale=12, color=C["ink"], lw=1.4, zorder=6))
ax2.text(mx + 0.5 * tx / n + 0.05, mz + 0.45 * tz / n, "토크\n(μ × B₀)", fontsize=8.5, va="center")
ax2.add_patch(Arc((0, 0), 0.9, 0.9, theta1=np.rad2deg(np.arctan2(mz, mx)), theta2=90, lw=0.9))
ax2.text(0.13, 0.5, "θ", fontsize=10)
ax2.text(-1.25, 1.62, "끝이 원을 그린다\nω = γB₀ (θ와 무관)", fontsize=8.5, color=C["ink"])
ax2.text(0, -0.25, "토크는 μ를 B₀ 쪽으로 넘기지 않고\n옆으로 민다", ha="center", va="top", fontsize=8.5)
ax2.set_xlim(-1.4, 1.6)
ax2.set_ylim(-0.75, 2.1)
ax2.set_aspect("equal")
ax2.axis("off")
ax2.set_title("(나) 자기장 속의 세차 운동", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
