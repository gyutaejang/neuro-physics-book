from figstyle import plt, np, save, C
from matplotlib.patches import Ellipse, FancyArrowPatch, Polygon


def arrow(ax, p0, p1, color, lw=1.6, style="-|>", **kw):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, color=color, lw=lw, mutation_scale=11, **kw))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.3), gridspec_kw={"width_ratios": [1, 1.25]})

# 왼쪽: 머리 옆모습(오른쪽 얼굴이 보는 사람 쪽)과 RAS 축
a1.add_patch(Ellipse((0, 0), 2.0, 2.3, fc=C["light"], ec=C["gray"], lw=1))
a1.add_patch(Polygon([[0.97, 0.15], [1.18, -0.12], [0.95, -0.25]], closed=True, fc=C["light"], ec=C["gray"],
                     lw=1))
arrow(a1, (0, 0), (1.75, 0), C["blue"])
arrow(a1, (0, 0), (0, 1.75), C["blue"])
arrow(a1, (0, 0), (-0.95, -1.15), C["blue"])
a1.text(1.78, 0.08, "y\n앞(A)", fontsize=8.5, color=C["blue"], va="bottom")
a1.text(0.08, 1.78, "z  위(S)", fontsize=8.5, color=C["blue"])
a1.text(-1.0, -1.25, "x  오른쪽(R)\n(보는 사람 쪽)", fontsize=8.5, color=C["blue"], ha="center", va="top")
# 회전 표시
arrow(a1, (-1.2, 0.55), (-1.2, -0.55), C["purple"], lw=1.1, connectionstyle="arc3,rad=0.6")
a1.text(-1.62, 0.0, "피치\n(x축,\n끄덕임)", fontsize=7.5, color=C["purple"], ha="right", va="center")
arrow(a1, (-0.3, 1.45), (0.3, 1.45), C["purple"], lw=1.1, connectionstyle="arc3,rad=0.9")
a1.text(0.38, 1.4, "요 (z축, 도리도리)", fontsize=7.5, color=C["purple"])
arrow(a1, (1.45, 0.3), (1.45, -0.3), C["purple"], lw=1.1, connectionstyle="arc3,rad=-0.9")
a1.text(1.4, -0.5, "롤\n(y축, 갸웃)", fontsize=7.5, color=C["purple"], va="top")
a1.set_xlim(-2.45, 2.4)
a1.set_ylim(-2.0, 2.1)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("평행이동 3 + 회전 3 = 6 파라미터", fontsize=9.5)

# 오른쪽: 틀별 변위(FD) 시계열
rng = np.random.default_rng(3)
n = 240
fd = np.abs(rng.normal(0.09, 0.04, n))
for i, h in ((52, 0.62), (53, 0.35), (131, 0.9), (132, 0.48), (190, 0.55)):
    fd[i] = h
a2.plot(np.arange(n), fd, color=C["blue"], lw=0.9)
a2.axhline(0.5, color=C["red"], ls="--", lw=0.9)
a2.text(92, 0.53, "기준 0.5 mm", ha="center", fontsize=8, color=C["red"])
over = np.where(fd > 0.5)[0]
a2.scatter(over, fd[over], color=C["red"], s=14, zorder=3)
a2.annotate("짧은 움직임\n(기침, 침 삼킴)", xy=(131, 0.9), xytext=(150, 0.82), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.set_xlabel("볼륨 번호 (TR마다 하나)")
a2.set_ylabel("틀별 변위 FD (mm)")
a2.set_ylim(0, 1.0)
a2.set_title("움직임을 숫자 하나로: FD", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
