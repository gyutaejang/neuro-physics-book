from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.6), gridspec_kw=dict(width_ratios=[1, 1.25]))


def neuron(ax, x0, y0, s=1.0, lw=1.2):
    ax.add_patch(plt.Polygon([[x0 - 0.22 * s, y0], [x0 + 0.22 * s, y0], [x0, y0 + 0.4 * s]],
                             facecolor=C["green"], edgecolor=C["green"], alpha=0.85))
    ax.plot([x0, x0], [y0 + 0.4 * s, y0 + 2.6 * s], color=C["green"], lw=lw)
    for dx in (-0.35, 0, 0.35):
        ax.plot([x0, x0 + dx * s], [y0 + 2.6 * s, y0 + 3.0 * s], color=C["green"], lw=lw * 0.8)
    for dx in (-0.35, 0.35):
        ax.plot([x0, x0 + dx * s], [y0, y0 - 0.35 * s], color=C["green"], lw=lw * 0.8)


# 왼쪽: 피라미드 뉴런 하나
neuron(a1, 0, 0, 1.0, 1.6)
a1.text(-0.25, 2.75, "−", fontsize=16, color=C["red"], weight="bold", ha="right", va="center")
a1.text(-0.25, 0.25, "+", fontsize=16, color=C["blue"], weight="bold", ha="right", va="center")
a1.text(0.55, 2.75, "흥분성 시냅스 입력\n(양이온이 들어감:\n밖은 −, 흡입원)", fontsize=8, va="center")
a1.text(0.55, 0.15, "전류가 빠져나옴\n(밖은 +, 방출원)", fontsize=8, va="center")
a1.annotate("", xy=(-1.0, 0.3), xytext=(-1.0, 2.7),
            arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=2, mutation_scale=14))
a1.text(-1.15, 1.5, "등가 쌍극자", rotation=90, fontsize=8.5, color=C["blue"], ha="right", va="center")
a1.set_xlim(-1.9, 2.4)
a1.set_ylim(-0.7, 3.4)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("뉴런 하나", fontsize=10)

# 오른쪽: 접힌 피질에서 쌍극자 방향
x = np.linspace(0, 4 * np.pi, 400)
A = 1.4
yb = A * np.cos(x)
a2.fill_between(x, yb - 0.55, yb + 0.55, color=C["green"], alpha=0.15, lw=0)
a2.plot(x, yb + 0.55, color=C["green"], lw=0.8)
a2.plot(x, yb - 0.55, color=C["green"], lw=0.8)
for xi in np.linspace(0.25, 4 * np.pi - 0.25, 22):
    slope = -A * np.sin(xi)
    n = np.array([-slope, 1.0]) / np.hypot(slope, 1.0)  # 표면에 수직
    y0 = A * np.cos(xi)
    tang = abs(n[0]) > 0.6
    col = C["purple"] if tang else C["blue"]
    a2.annotate("", xy=(xi + 0.42 * n[0], y0 + 0.42 * n[1]), xytext=(xi - 0.42 * n[0], y0 - 0.42 * n[1]),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2, mutation_scale=8))
a2.plot([0, 4 * np.pi], [2.5, 2.5], color=C["gray"], lw=3, alpha=0.5)
a2.text(2 * np.pi, 2.65, "두피", ha="center", va="bottom", fontsize=8.5, color=C["gray"])
a2.text(2 * np.pi, -2.25, "이랑 꼭대기: 두피에 수직 (파랑)\n고랑 벽: 두피에 나란 (보라)", ha="center",
        va="top", fontsize=8.5)
a2.set_xlim(-0.2, 4 * np.pi + 0.2)
a2.set_ylim(-3.2, 3.0)
a2.axis("off")
a2.set_title("접힌 피질: 쌍극자 방향이 위치마다 다르다", fontsize=10)
fig.tight_layout()
save(fig, __file__)
