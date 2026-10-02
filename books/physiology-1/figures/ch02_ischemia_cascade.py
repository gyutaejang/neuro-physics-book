from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(7.4, 3.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 7.4)
ax.axis("off")
W, H = 3.3, 1.35


def box(x, y, text, col, fill=0.18):
    ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.04,rounding_size=0.25",
                                fc=col, ec=col, alpha=fill, lw=0))
    ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.04,rounding_size=0.25",
                                fc="none", ec=col, lw=0.9))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.3, color=C["ink"])


def arr(p, q, col=C["gray"]):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2, mutation_scale=11))


xs = [2.0, 6.0, 10.0, 14.0]
y1, y2, y3 = 6.3, 3.85, 1.2
row1 = ["혈류 차단\n(뇌졸중, 심정지)", "ATP 고갈\n(수 분 안)", "Na⁺/K⁺ 펌프 정지", "Na⁺ 들어오고 K⁺ 나감\n이온 기울기 붕괴"]
for x, t in zip(xs, row1):
    box(x, y1, t, C["red"] if x < 7 else C["green"])
for a, b in zip(xs[:-1], xs[1:]):
    arr((a + W / 2, y1), (b - W / 2, y1))

row2 = [(14.0, "막 탈분극\n(무산소 탈분극)", C["green"]), (10.0, "Cl⁻과 물이\n따라 들어온다", C["green"]),
        (6.0, "세포가 붓는다\n(세포독성 부종)", C["green"]), (2.0, "DWI 고신호\nADC 약 30–50% 감소", C["purple"])]
for x, t, col in row2:
    box(x, y2, t, col)
arr((14.0, y1 - H / 2), (14.0, y2 + H / 2))
for (a, _, _), (b, _, _) in zip(row2[:-1], row2[1:]):
    arr((a - W / 2, y2), (b + W / 2, y2))

row3 = [(14.0, "글루탐산 방출,\n운반체 역주행", C["green"]), (10.0, "Ca²⁺ 과부하\n흥분독성 (5장)", C["red"]),
        (6.0, "수 시간 뒤 혈관에서\nNa⁺·물 유입", C["green"]), (2.0, "²³Na MRI\n조직 Na⁺ 증가", C["purple"])]
for x, t, col in row3:
    box(x, y3, t, col)
arr((14.0, y2 - H / 2), (14.0, y3 + H / 2))
arr((14.0 - W / 2, y3), (10.0 + W / 2, y3))
arr((6.0, y2 - H / 2), (6.0, y3 + H / 2))
arr((6.0 - W / 2, y3), (2.0 + W / 2, y3))
save(fig, __file__)
