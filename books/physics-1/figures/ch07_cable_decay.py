from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch


def resistor(ax, p0, p1, n=4, w=0.1, color=None):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    u = d / np.hypot(*d)
    nrm = np.array([-u[1], u[0]])
    a, b = p0 + 0.2 * d, p0 + 0.8 * d
    pts = [p0, a] + [a + k / (2 * n) * (b - a) + nrm * w * (1 if k % 2 else -1) for k in range(1, 2 * n)] + [b, p1]
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color or C["ink"], lw=1.3)


fig = plt.figure(figsize=(7.2, 4.6))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.35], hspace=0.35)
a1 = fig.add_subplot(gs[0])
a2 = fig.add_subplot(gs[1])

# (가) 사다리 회로
n = 5
top, bot = 1.0, 0.0
for k in range(n):
    x0 = 0.6 + k * 1.3
    resistor(a1, (x0, top), (x0 + 1.3, top), color=C["blue"])
    resistor(a1, (x0 + 1.3, top), (x0 + 1.3, bot), n=3, color=C["green"])
    a1.plot([x0 + 1.3], [top], "o", color=C["ink"], ms=2.5)
a1.plot([0.6 + 1.3 * n, 0.6 + 1.3 * n + 0.5], [top, top], color=C["ink"], lw=1.3, ls=":")
a1.plot([0.6, 0.6 + 1.3 * n + 0.5], [bot, bot], color=C["ink"], lw=1.3)
a1.annotate("", xy=(0.6, top), xytext=(-0.1, top),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.3))
a1.text(-0.15, top + 0.18, "주입 전류", fontsize=8.5, color=C["red"])
a1.text(1.25, top + 0.22, "$r_i$ 축 방향 저항 (세포 속)", fontsize=8.5, color=C["blue"])
a1.text(2.0 + 0.1, 0.5, "$r_m$ 막 저항\n(새는 길)", fontsize=8.5, color=C["green"], va="center")
a1.text(4.0, bot - 0.22, "세포 밖 (접지로 둔다)", fontsize=8.5, ha="center", va="top")
a1.set_xlim(-0.4, 8.0)
a1.set_ylim(-0.6, 1.5)
a1.axis("off")
a1.set_title("(가) 수상돌기와 축삭은 새는 케이블이다", fontsize=10)

# (나) 지수 감쇠
x = np.linspace(0, 3, 300)
for lam, ls, lab in [(0.35, ":", "λ = 0.35 mm (가는 가지)"), (0.7, "-", "λ = 0.7 mm"),
                     (1.4, "--", "λ = 1.4 mm (굵은 가지)")]:
    a2.plot(x, 100 * np.exp(-x / lam), color=C["blue"], ls=ls, label=lab)
a2.axhline(100 * np.exp(-1), color=C["gray"], lw=0.6, ls=":")
a2.plot([0.7], [100 * np.exp(-1)], "o", color=C["red"], ms=4)
a2.annotate("x = λ에서 37%", xy=(0.7, 36.8), xytext=(1.05, 55), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.set_xlabel("주입 지점에서의 거리 x (mm)")
a2.set_ylabel("남은 전압 (%)")
a2.set_xlim(0, 3)
a2.set_ylim(0, 105)
a2.legend(fontsize=8, loc="upper right")
a2.set_title("(나) 정상 상태 전압은 거리에 따라 지수로 준다", fontsize=10)
save(fig, __file__)
