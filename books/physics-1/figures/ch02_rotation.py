from figstyle import plt, np, save, C
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon


def arrow(ax, p0, p1, color, lw=1.8, **kw):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", color=color, lw=lw, mutation_scale=12, **kw))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.4))

# 왼쪽: 등속 원운동
a1.add_patch(Circle((0, 0), 1, fill=False, ec=C["gray"], lw=1))
th = np.radians(40)
p = np.array([np.cos(th), np.sin(th)])
tang = np.array([-np.sin(th), np.cos(th)])
a1.plot([0, p[0]], [0, p[1]], color=C["gray"], lw=0.8)
a1.text(0.32, 0.12, "r", fontsize=10)
a1.scatter([p[0]], [p[1]], color=C["ink"], s=22, zorder=4)
arrow(a1, p, p + 0.75 * tang, C["blue"])
a1.text(*(p + 0.8 * tang + np.array([0.05, 0.05])), "속도 v = ωr\n(접선 방향)", fontsize=8, color=C["blue"])
arrow(a1, p, p * 0.45, C["red"])
a1.text(0.62, 0.22, "가속도\nv²/r\n(중심 쪽)", fontsize=8, color=C["red"], va="top")
arrow(a1, (0.25, -0.25), (-0.25, -0.25), C["purple"], lw=1.1, connectionstyle="arc3,rad=-0.8")
a1.text(0, -0.62, "각속도 ω", fontsize=8.5, color=C["purple"], ha="center")
a1.set_xlim(-1.4, 1.9)
a1.set_ylim(-1.3, 1.9)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("등속 원운동", fontsize=10)

# 오른쪽: 팽이의 세차 운동
tilt = np.radians(28)
u = np.array([np.sin(tilt), np.cos(tilt)])
n = np.array([np.cos(tilt), -np.sin(tilt)])
body = [u * 0.03, u * 0.6 + n * 0.5, u * 0.78 + n * 0.5, u * 0.9 + n * 0.2, u * 0.9 - n * 0.2,
        u * 0.78 - n * 0.5, u * 0.6 - n * 0.5]
a2.add_patch(Polygon(body, closed=True, fc=C["light"], ec=C["gray"], lw=1))
a2.plot([0, u[0] * 1.25], [0, u[1] * 1.25], color=C["ink"], lw=1.2)
a2.plot([-0.9, 0.9], [0, 0], color=C["gray"], lw=0.8)
arrow(a2, u * 1.25, u * 2.05, C["purple"], lw=2.2)
a2.text(*(u * 2.05 + np.array([0.08, -0.05])), "각운동량 L\n(회전축 방향)", fontsize=8, color=C["purple"])
cm = u * 0.68
arrow(a2, cm, cm + np.array([0, -0.85]), C["red"])
a2.text(cm[0] + 0.08, cm[1] - 0.75, "중력 mg", fontsize=8, color=C["red"])
L_tip = u * 2.05
a2.add_patch(Ellipse((0, L_tip[1]), 2 * L_tip[0], 0.38, fill=False, ec=C["purple"], ls="--", lw=0.9))
arrow(a2, (-0.25, L_tip[1] - 0.188), (0.25, L_tip[1] - 0.188), C["purple"], lw=1.0)
a2.text(-0.98, L_tip[1] + 0.25, "세차: L의 끝이\n원을 그린다", fontsize=8, color=C["purple"], ha="center")
a2.plot([0, 0], [0, L_tip[1] + 0.3], color=C["gray"], lw=0.6, ls=":")
a2.text(-0.75, 0.55, "토크 = 중력 × 팔 길이\n→ L을 옆으로 민다", fontsize=7.5, color=C["red"], ha="center")
a2.set_xlim(-1.7, 1.9)
a2.set_ylim(-0.2, 2.6)
a2.set_aspect("equal")
a2.axis("off")
a2.set_title("팽이의 세차 운동", fontsize=10)
fig.tight_layout()
save(fig, __file__)
