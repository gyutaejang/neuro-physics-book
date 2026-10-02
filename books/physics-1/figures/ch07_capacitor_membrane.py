from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw={"width_ratios": [1, 1.25]})

# (가) 평행판 축전기
for y, sgn, col in [(1.0, "+", C["red"]), (0.0, "−", C["blue"])]:
    a1.add_patch(Rectangle((0, y - 0.04), 2.4, 0.08, color=C["gray"]))
    for x in np.linspace(0.2, 2.2, 7):
        a1.text(x, y + (0.16 if sgn == "+" else -0.16), sgn, ha="center", va="center",
                fontsize=11, color=col)
for x in np.linspace(0.35, 2.05, 5):
    a1.annotate("", xy=(x, 0.1), xytext=(x, 0.9),
                arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1))
a1.annotate("", xy=(2.55, 0.0), xytext=(2.55, 1.0), arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8))
a1.text(2.65, 0.5, "d", va="center", fontsize=10)
a1.text(1.2, 1.42, "넓이 A인 판 두 장, +Q와 −Q", ha="center", fontsize=8.5)
a1.text(1.2, -0.48, "사이는 절연체 (전기장 E)", ha="center", fontsize=8.5, color=C["blue"])
a1.text(1.2, -0.85, r"$C = \varepsilon_0 \varepsilon_r A / d$", ha="center", fontsize=10.5)
a1.set_xlim(-0.2, 3.0)
a1.set_ylim(-1.05, 1.65)
a1.set_title("(가) 평행판 축전기", fontsize=10)
a1.axis("off")

# (나) 세포막
a2.add_patch(Rectangle((0, 1.0), 3.2, 0.9, color=C["light"], lw=0))
a2.add_patch(Rectangle((0, -1.0), 3.2, 0.62, color=C["light"], lw=0))
xs = np.linspace(0.12, 3.08, 15)
for x in xs:
    for yh, sgn in [(0.88, -1), (-0.26, 1)]:
        a2.plot([x - 0.04, x - 0.04], [yh, yh + sgn * 0.5 * (1 if sgn > 0 else 1)], color="#c9a96e", lw=1)
        a2.plot([x + 0.04, x + 0.04], [yh, yh + sgn * 0.5], color="#c9a96e", lw=1)
        a2.add_patch(Circle((x, yh), 0.085, color=C["green"], alpha=0.75, lw=0))
for x in np.linspace(0.25, 2.95, 7):
    a2.text(x, 1.2, "+", ha="center", va="center", fontsize=11, color=C["red"])
    a2.text(x, -0.55, "−", ha="center", va="center", fontsize=11, color=C["blue"])
a2.text(1.6, 1.62, "세포 밖: 세포외액 (도체)", ha="center", fontsize=8.5)
a2.text(1.6, -0.86, "세포 안: 세포질 (도체)", ha="center", fontsize=8.5)
a2.annotate("", xy=(3.38, -0.3), xytext=(3.38, 0.92), arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8))
a2.text(3.48, 0.31, "지질 이중층\n(절연체)\n~5 nm", va="center", fontsize=8)
a2.set_xlim(-0.1, 4.4)
a2.set_ylim(-1.05, 1.95)
a2.set_title("(나) 세포막도 축전기다", fontsize=10)
a2.axis("off")
fig.tight_layout()
save(fig, __file__)
