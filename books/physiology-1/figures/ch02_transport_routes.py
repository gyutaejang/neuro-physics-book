from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(7.4, 3.6))
ax.set_xlim(-1.4, 15)
ax.set_ylim(-2.3, 5.0)
ax.axis("off")

# 막: 지질 이중층 띠
y0, y1 = 1.2, 2.6
ax.add_patch(Rectangle((0, y0), 15, y1 - y0, color=C["green"], alpha=0.12, lw=0, zorder=0))
for x in np.arange(0.15, 15, 0.3):
    for y, d in ((y1, -1), (y0, 1)):
        ax.plot([x], [y], "o", color=C["green"], ms=3.2, alpha=0.6, zorder=1)
        ax.plot([x, x], [y, y + d * 0.45], color=C["green"], lw=0.6, alpha=0.5, zorder=1)
ax.text(-0.2, 3.6, "세포 밖", fontsize=9, va="center", ha="right")
ax.text(-0.2, 0.3, "세포 안", fontsize=9, va="center", ha="right")

def arrow(x0, ya, yb, col, lw=1.6):
    ax.annotate("", xy=(x0, yb), xytext=(x0, ya),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=12), zorder=5)

def protein(xc, w=1.1, col=C["blue"], gap=0.0):
    for xl in (xc - gap / 2 - w / 2, xc + gap / 2):
        ax.add_patch(FancyBboxPatch((xl, y0 - 0.35), w / 2, y1 - y0 + 0.7,
                                    boxstyle="round,pad=0.05,rounding_size=0.2",
                                    fc=col, ec="none", alpha=0.35, zorder=2))

# (가) 단순 확산
x = 1.6
arrow(x, 3.9, 0.3, C["ink"])
ax.text(x + 0.25, 4.1, "O$_2$, CO$_2$", fontsize=8.5, va="center")
ax.text(x + 0.4, 3.35, "지질에 녹는\n약물", fontsize=7.5, va="center", color=C["gray"])

# (나) 통로
x = 4.4
protein(x, w=1.3, col=C["blue"], gap=0.5)
arrow(x, 0.3, 3.9, C["green"])
ax.text(x + 0.85, 3.6, "K⁺", fontsize=9, color=C["green"], va="center")
ax.text(x, -0.75, "10⁶–10⁸ 개/s", fontsize=7.5, ha="center", color=C["gray"])

# (다) 운반체
x = 7.0
ax.add_patch(FancyBboxPatch((x - 0.6, y0 - 0.35), 1.2, y1 - y0 + 0.7, boxstyle="round,pad=0.05,rounding_size=0.3",
                            fc=C["purple"], ec="none", alpha=0.3, zorder=2))
ax.add_patch(plt.Polygon([[x - 0.25, y1 + 0.35], [x + 0.25, y1 + 0.35], [x, y1 - 0.2]], fc="white", ec="none", zorder=3))
arrow(x, 3.9, 0.3, C["ink"])
ax.text(x + 0.25, 4.1, "포도당", fontsize=8.5, va="center")
ax.text(x, -0.75, "10²–10⁴ 개/s", fontsize=7.5, ha="center", color=C["gray"])

# (라) 펌프
x = 9.9
ax.add_patch(FancyBboxPatch((x - 0.75, y0 - 0.35), 1.5, y1 - y0 + 0.7, boxstyle="round,pad=0.05,rounding_size=0.3",
                            fc=C["red"], ec="none", alpha=0.3, zorder=2))
arrow(x - 0.35, 0.3, 3.9, C["green"])
arrow(x + 0.35, 3.9, 0.3, C["green"])
ax.text(x - 0.45, 4.15, "3 Na⁺", fontsize=8.5, color=C["green"], ha="right", va="center")
ax.text(x + 0.45, 4.15, "2 K⁺", fontsize=8.5, color=C["green"], ha="left", va="center")
ax.text(x, 0.55, "ATP→ADP", fontsize=7.5, ha="center", va="center", color=C["red"],
        bbox=dict(fc="white", ec="none", pad=0.5), zorder=6)
ax.text(x, -0.75, "약 100 회/s", fontsize=7.5, ha="center", color=C["gray"])

# (마) 2차 능동 수송
x = 13.0
ax.add_patch(FancyBboxPatch((x - 0.75, y0 - 0.35), 1.5, y1 - y0 + 0.7, boxstyle="round,pad=0.05,rounding_size=0.3",
                            fc=C["purple"], ec="none", alpha=0.3, zorder=2))
arrow(x - 0.35, 3.9, 0.3, C["green"])
arrow(x + 0.35, 3.9, 0.3, C["ink"])
ax.text(x - 0.45, 4.15, "Na⁺", fontsize=8.5, color=C["green"], ha="right", va="center")
ax.text(x + 0.45, 4.15, "글루탐산", fontsize=8.5, ha="left", va="center")

names = [(1.6, "(가) 단순 확산"), (4.4, "(나) 통로"), (7.0, "(다) 운반체\n(촉진 확산)"),
         (9.9, "(라) 펌프\n(1차 능동)"), (13.0, "(마) 공동 수송\n(2차 능동)")]
for x, n in names:
    ax.text(x, -1.05, n, ha="center", va="top", fontsize=8.5)

# 수동/능동 괄호
for xa, xb, lab, col in ((0.8, 7.9, "수동: 기울기를 따라 내려간다", C["gray"]),
                          (8.9, 14.2, "능동: 기울기를 거슬러 올린다", C["red"])):
    ax.plot([xa, xa, xb, xb], [4.55, 4.75, 4.75, 4.55], color=col, lw=0.9)
    ax.text((xa + xb) / 2, 4.85, lab, ha="center", va="bottom", fontsize=8.5, color=col)
ax.set_ylim(-2.0, 5.4)
save(fig, __file__)
