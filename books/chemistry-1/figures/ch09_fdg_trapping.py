from matplotlib.patches import FancyBboxPatch

from figstyle import plt, save, C

fig, ax = plt.subplots(figsize=(7.2, 3.3))
ax.set_xlim(0, 10.6)
ax.set_ylim(0, 4.6)
ax.axis("off")

# 혈관과 세포
ax.add_patch(FancyBboxPatch((0.1, 0.25), 1.7, 3.9, boxstyle="round,pad=0.02,rounding_size=0.25",
                            fc=C["red"], alpha=0.10, ec="none"))
ax.text(0.95, 4.33, "혈액", ha="center", fontsize=9.5)
ax.add_patch(FancyBboxPatch((2.6, 0.25), 7.9, 3.9, boxstyle="round,pad=0.02,rounding_size=0.25",
                            fc=C["green"], alpha=0.10, ec=C["green"], lw=1.2))
ax.text(6.55, 4.33, "뇌세포 (뉴런, 성상교세포)", ha="center", fontsize=9.5, color=C["green"])

def box(x, y, t, col, w=1.25):
    ax.text(x, y, t, ha="center", va="center", fontsize=9, color=col,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=col, lw=1.1))

def arrow(x0, y0, x1, y1, col, txt=None, ty=0.2, both=False):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="<|-|>" if both else "-|>", color=col, lw=1.4, mutation_scale=11))
    if txt:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + ty, txt, ha="center", va="bottom", fontsize=7.8, color=C["ink"])

yg, yf = 3.0, 1.2
# 포도당 경로
box(0.95, yg, "포도당", C["blue"])
arrow(1.6, yg, 3.55, yg, C["blue"], "GLUT 운반체", both=True)
box(4.2, yg, "포도당", C["blue"])
arrow(4.85, yg, 6.25, yg, C["blue"], "헥소키나아제\n(+ATP)")
box(7.0, yg, "포도당-6-인산", C["blue"], )
arrow(7.95, yg, 9.1, yg, C["blue"], "이성질화효소")
ax.text(9.75, yg, "해당 작용\n→ 피루브산", ha="center", va="center", fontsize=8.5, color=C["blue"])

# FDG 경로
box(0.95, yf, "FDG", C["red"])
arrow(1.6, yf, 3.55, yf, C["red"], "GLUT 운반체", both=True)
box(4.2, yf, "FDG", C["red"])
arrow(4.85, yf, 6.25, yf, C["red"], "헥소키나아제\n(+ATP)")
box(7.0, yf, "FDG-6-인산", C["red"])
ax.annotate("", xy=(9.1, yf), xytext=(7.95, yf),
            arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=1.2, ls="--", mutation_scale=11))
ax.text(8.52, yf, "✕", ha="center", va="center", fontsize=15, color=C["red"])
ax.text(9.75, yf, "다음 단계로\n못 간다", ha="center", va="center", fontsize=8.5, color=C["red"])
ax.text(7.0, 0.45, "음전하 인산기 → 운반체로 못 나감 → 세포에 갇혀 쌓인다",
        ha="center", va="center", fontsize=8.3, color=C["red"])
ax.text(2.2, 2.1, "혈액뇌\n장벽", ha="center", va="center", fontsize=7.8, color=C["gray"])
save(fig, __file__)
