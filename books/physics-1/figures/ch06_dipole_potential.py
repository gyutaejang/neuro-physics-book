from figstyle import plt, np, save, C
from matplotlib.colors import LinearSegmentedColormap

cmap = LinearSegmentedColormap.from_list("rb", [C["red"], "white", C["blue"]])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[1.05, 1]))

# 왼쪽: 쌍극자 주변의 전위 (위가 +, 아래가 −)
d = 0.3
x, y = np.meshgrid(np.linspace(-2, 2, 400), np.linspace(-2, 2, 400))
V = 1 / np.hypot(x, y - d) - 1 / np.hypot(x, y + d)
Vc = np.clip(V, -3, 3)
a1.contourf(x, y, Vc, levels=np.linspace(-3, 3, 25), cmap=cmap)
lv = [-2, -1, -0.5, -0.25, -0.12, 0.12, 0.25, 0.5, 1, 2]
a1.contour(x, y, V, levels=lv, colors=C["ink"], linewidths=0.5)
a1.contour(x, y, V, levels=[0], colors=C["gray"], linewidths=1, linestyles="--")
for s, yy in ((+1, d), (-1, -d)):
    a1.add_patch(plt.Circle((0, yy), 0.11, facecolor="white", edgecolor=C["ink"], lw=1, zorder=5))
    a1.text(0, yy, "+" if s > 0 else "−", ha="center", va="center", fontsize=9, weight="bold", zorder=6)
a1.text(1.95, 0.08, "전위 0인 면", ha="right", va="bottom", fontsize=8.5, color=C["gray"])
a1.text(0, 1.75, "전위 +", ha="center", fontsize=9, color=C["blue"])
a1.text(0, -1.9, "전위 −", ha="center", fontsize=9, color=C["red"])
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("검은 선 = 등전위선", fontsize=10)

# 오른쪽: 거리에 따른 감소
r = np.logspace(0, 1, 100)
a2.loglog(r, 1 / r, color=C["green"], label="전하 하나: 1/r")
a2.loglog(r, 1 / r ** 2, color=C["blue"], label="쌍극자: 1/r²")
for rr in (1, 2):
    a2.scatter([rr, rr], [1 / rr, 1 / rr ** 2], color=[C["green"], C["blue"]], s=16, zorder=3)
a2.text(2.15, 0.5, "거리 2배 → 1/2", fontsize=8.5, color=C["green"], va="center")
a2.text(2.15, 0.25, "거리 2배 → 1/4", fontsize=8.5, color=C["blue"], va="center")
a2.set_xlabel("거리 (기준 거리의 배수)")
a2.set_ylabel("전위 (기준 거리에서 1)")
a2.set_ylim(5e-3, 1.5)
a2.set_xticks([1, 2, 5, 10])
a2.set_xticklabels(["1", "2", "5", "10"])
a2.set_yticks([1, 0.1, 0.01])
a2.set_yticklabels(["1", "0.1", "0.01"])
a2.minorticks_off()
a2.legend(loc="lower left", fontsize=8.5)
a2.set_title("멀어질 때 줄어드는 빠르기", fontsize=10)
fig.tight_layout()
save(fig, __file__)
