from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [1, 2.1]})

# 왼쪽: 용수철에 매달린 물체 (세 순간)
a1.set_xlim(-0.2, 3.4)
a1.set_ylim(-1.75, 2.1)
a1.axis("off")
a1.plot([-0.1, 3.3], [1.95, 1.95], color=C["ink"], lw=2)
for i, x in enumerate((0.0, 1.0, -1.0)):
    cx = 0.5 + i * 1.1
    top, bot = 1.95, x + 0.25
    n = 9
    ys = np.linspace(top, bot, 2 * n + 1)
    xs = cx + np.array([0] + [0.12 * (-1) ** k for k in range(2 * n - 1)] + [0])
    a1.plot(xs, ys, color=C["gray"], lw=1)
    a1.add_patch(Rectangle((cx - 0.25, x - 0.25), 0.5, 0.5, color=C["blue"], alpha=0.85))
a1.axhline(0, xmin=0.02, xmax=0.98, color=C["red"], lw=0.8, ls="--")
a1.text(1.05, 0.05, "평형", fontsize=8.5, color=C["red"], ha="center", va="bottom")
for i, lab in enumerate(("x = 0", "x = +A", "x = −A")):
    a1.text(0.5 + i * 1.1, -1.55, lab, ha="center", fontsize=8.5)
a1.set_title("용수철과 물체", fontsize=10)

# 오른쪽: 위치-시간 그래프
t = np.linspace(0, 2.6, 600)
T = 1.0
x = np.cos(2 * np.pi * t / T)
a2.plot(t, x, color=C["blue"], lw=1.8)
a2.axhline(0, color=C["gray"], lw=0.6)
a2.set_xlabel("시간 t (s)")
a2.set_ylabel("위치 x")
a2.set_yticks([-1, 0, 1])
a2.set_yticklabels(["−A", "0", "+A"])
a2.set_ylim(-2.35, 1.55)
a2.annotate("", xy=(1.0, 1.25), xytext=(2.0, 1.25), arrowprops=dict(arrowstyle="<->", color=C["red"]))
a2.text(1.5, 1.3, "주기 T", ha="center", va="bottom", fontsize=9, color=C["red"])
a2.annotate("", xy=(0.5, 0), xytext=(0.5, 1), arrowprops=dict(arrowstyle="<->", color=C["red"]))
a2.plot([0.0, 0.5], [1, 1], color=C["gray"], lw=0.6, ls=":")
a2.text(0.55, 0.5, "진폭 A", fontsize=9, color=C["red"], va="center")
for (px, py), (tx, ty), lab in (((0.5, -1), (0.5, -1.62), "양 끝: 잠시 멈춤\n되돌리는 힘 최대"),
                                 ((1.75, 0), (2.05, -1.62), "평형: 속력 최대\n되돌리는 힘 0")):
    a2.plot([px], [py], "o", color=C["ink"], ms=3.5, zorder=4)
    a2.annotate(lab, xy=(px, py), xytext=(tx, ty), fontsize=8, color="#444", ha="center", va="top",
                arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.7, shrinkB=3))
a2.set_title("위치는 사인 곡선을 그린다", fontsize=10)
fig.tight_layout()
save(fig, __file__)
