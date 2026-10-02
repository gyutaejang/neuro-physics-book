from figstyle import plt, np, save, C


def arrow(ax, x0, y0, x1, y1, color, lw=1.8):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.1))

# 왼쪽: 머리-꼬리 잇기로 더하기
arrow(a1, 0, 0, 3, 1, C["blue"])
arrow(a1, 3, 1, 4, 3, C["blue"])
arrow(a1, 0, 0, 4, 3, C["red"], lw=2.2)
a1.text(1.6, 0.25, r"$\vec{A}$ = (3, 1)", fontsize=9, color=C["blue"])
a1.text(3.6, 1.7, r"$\vec{B}$ = (1, 2)", fontsize=9, color=C["blue"])
a1.text(0.6, 2.0, r"$\vec{A}+\vec{B}$ = (4, 3)", fontsize=9, color=C["red"])
a1.text(0.6, 1.55, "크기 5", fontsize=8.5, color=C["red"])
a1.set_title("더하기: 꼬리를 앞 화살표의 머리에")

# 오른쪽: 성분
arrow(a2, 0, 0, 4, 3, C["red"], lw=2.2)
a2.plot([4, 4], [0, 3], color=C["gray"], ls="--", lw=0.9)
a2.plot([0, 4], [3, 3], color=C["gray"], ls="--", lw=0.9)
arrow(a2, 0, 0, 4, 0, C["blue"], lw=1.4)
arrow(a2, 0, 0, 0, 3, C["blue"], lw=1.4)
th = np.linspace(0, np.arctan2(3, 4), 30)
a2.plot(1.0 * np.cos(th), 1.0 * np.sin(th), color=C["ink"], lw=0.8)
a2.text(1.1, 0.25, r"$\theta$", fontsize=10)
a2.text(2.0, -0.45, r"$x$ 성분 $= |\vec{v}|\cos\theta = 4$", ha="center", fontsize=8.5, color=C["blue"])
a2.text(-0.2, 1.5, r"$y$ 성분 = 3", ha="right", va="center", fontsize=8.5, color=C["blue"])
a2.text(1.7, 2.0, r"$|\vec{v}| = \sqrt{4^2+3^2} = 5$", fontsize=8.5, color=C["red"], ha="right")
a2.set_title("성분: 축 방향 그림자")

for ax, xl in ((a1, (-0.3, 5.3)), (a2, (-2.4, 5.0))):
    ax.set_xlim(*xl)
    ax.set_ylim(-0.8, 3.6)
    ax.set_aspect("equal")
    ax.axhline(0, color=C["gray"], lw=0.5)
    ax.axvline(0, color=C["gray"], lw=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
fig.tight_layout()
save(fig, __file__)
