from figstyle import plt, np, save, C

fig, axes = plt.subplots(1, 4, figsize=(7.4, 2.9))


def atom(ax, x, y, s, size=13, color=C["ink"]):
    ax.text(x, y, s, ha="center", va="center", fontsize=size, weight="bold", color=color, zorder=4,
            bbox=dict(boxstyle="circle,pad=0.12", facecolor="white", edgecolor="none"))


def line(ax, p, q, **kw):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=C["ink"], lw=1.8, zorder=2, **kw)


def wedge(ax, p, q, w=0.09):
    p, q = np.array(p), np.array(q)
    u = (q - p) / np.linalg.norm(q - p)
    v = np.array([-u[1], u[0]])
    ax.add_patch(plt.Polygon([p, q + v * w, q - v * w], color=C["ink"], zorder=2))


def dash(ax, p, q, n=7, w=0.09):
    p, q = np.array(p), np.array(q)
    u = (q - p) / np.linalg.norm(q - p)
    v = np.array([-u[1], u[0]])
    for t in np.linspace(0.15, 1, n):
        c = p + (q - p) * t
        ax.plot(*zip(c + v * w * t, c - v * w * t), color=C["ink"], lw=1.1, zorder=2)


def lone(ax, p, ang, L=0.62):
    t = np.radians(ang)
    from matplotlib.patches import Ellipse
    c = (p[0] + 0.62 * L * np.cos(t), p[1] + 0.62 * L * np.sin(t))
    ax.add_patch(Ellipse(c, L, 0.3, angle=ang, facecolor=C["light"], edgecolor=C["gray"], lw=0.8, zorder=1))
    for s in (-0.06, 0.06):
        ax.plot(c[0] - np.sin(t) * s, c[1] + np.cos(t) * s, "o", color=C["red"], ms=2.5, zorder=3)


# 메테인: 사면체
ax = axes[0]
c = (0, 0)
line(ax, c, (0, 0.95)); line(ax, c, (-0.85, -0.4))
wedge(ax, c, (0.55, -0.6)); dash(ax, c, (0.85, -0.2))
atom(ax, 0, 0, "C"); atom(ax, 0, 0.95, "H"); atom(ax, -0.85, -0.4, "H"); atom(ax, 0.55, -0.6, "H"); atom(ax, 0.85, -0.2, "H")
ax.set_title("메테인 CH$_4$\n사면체, 109.5°", fontsize=9.5)
# 암모니아
ax = axes[1]
lone(ax, c, 90)
line(ax, c, (-0.85, -0.45)); wedge(ax, c, (0.45, -0.75)); dash(ax, c, (0.85, -0.35))
atom(ax, 0, 0, "N"); atom(ax, -0.85, -0.45, "H"); atom(ax, 0.45, -0.75, "H"); atom(ax, 0.85, -0.35, "H")
ax.set_title("암모니아 NH$_3$\n삼각뿔, 107°", fontsize=9.5)
# 물
ax = axes[2]
lone(ax, c, 60); lone(ax, c, 120)
h1 = (-0.9 * np.sin(np.radians(52.25)), -0.9 * np.cos(np.radians(52.25)))
h2 = (-h1[0], h1[1])
line(ax, c, h1); line(ax, c, h2)
atom(ax, 0, 0, "O"); atom(ax, *h1, "H"); atom(ax, *h2, "H")
ax.text(0.55, 0.55, "δ−", fontsize=10, color=C["red"])
ax.text(h1[0] - 0.2, h1[1] + 0.05, "δ+", fontsize=10, color=C["blue"], ha="right")
ax.text(h2[0] + 0.15, h2[1] + 0.05, "δ+", fontsize=10, color=C["blue"])
ax.annotate("", xy=(0, -1.15), xytext=(0, -0.2),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.8))
ax.text(0.08, -1.1, "p", fontsize=10, color=C["red"], style="italic")
ax.set_title("물 H$_2$O\n굽은 모양, 104.5°", fontsize=9.5)
# 이산화탄소
ax = axes[3]
for s in (-1, 1):
    ax.plot([0, s * 0.85], [0.05, 0.05], color=C["ink"], lw=1.6)
    ax.plot([0, s * 0.85], [-0.05, -0.05], color=C["ink"], lw=1.6)
atom(ax, 0, 0, "C"); atom(ax, -0.85, 0, "O"); atom(ax, 0.85, 0, "O")
ax.annotate("", xy=(0.15, -0.45), xytext=(0.75, -0.45), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.4))
ax.annotate("", xy=(-0.15, -0.45), xytext=(-0.75, -0.45), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.4))
ax.text(0, -0.75, "결합 쌍극자가 상쇄\n→ 분자 쌍극자 0", ha="center", va="top", fontsize=8, color=C["red"])
ax.set_title("이산화탄소 CO$_2$\n직선, 180°", fontsize=9.5)

for ax in axes:
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.4, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
fig.text(0.5, 0.06, "쐐기 = 종이 앞으로, 점선 = 종이 뒤로.  회색 타원 = 비공유 전자쌍.  빨간 화살표 p = 쌍극자 모멘트(− 에서 + 로)",
         ha="center", fontsize=8, color=C["gray"])
save(fig, __file__)
