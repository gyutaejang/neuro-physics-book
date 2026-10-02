from figstyle import plt, save, C
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(7.3, 3.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")


def box(x, y, w, h, text, col, alpha=0.18, fs=9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                fc=col, ec=col, alpha=alpha, lw=0))
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                fc="none", ec=col, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=C["ink"])


def arrow(x0, y0, x1, y1, col, lw):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=12, alpha=0.8))


box(0.1, 1.9, 1.8, 1.3, "포도당 + O$_2$\n화학 에너지\n약 20 W", C["blue"])
box(2.9, 3.2, 1.8, 1.1, "ATP에 담기는 몫\n대략 절반–60%", C["red"])
box(2.9, 0.4, 1.8, 1.1, "곧바로 열\n(합성 과정의 손실)", C["gray"])
box(5.6, 3.55, 2.1, 1.0, "Na⁺/K⁺ 펌프\nATP 사용의 절반 이상", C["green"])
box(5.6, 2.15, 2.1, 1.15, "기타 일\nCa²⁺ 펌프, 소포 재충전,\n단백질 합성 등", C["green"], fs=8.5)
box(8.4, 0.4, 1.5, 1.6, "모두 열\n약 20 W\n→ 혈류가\n실어 나른다", C["red"], alpha=0.12, fs=8.5)

arrow(1.95, 2.9, 2.85, 3.6, C["red"], 3)
arrow(1.95, 2.2, 2.85, 1.0, C["gray"], 3)
arrow(4.75, 3.95, 5.55, 4.05, C["green"], 2.5)
arrow(4.75, 3.45, 5.55, 2.8, C["green"], 2)
arrow(7.75, 3.9, 8.75, 2.05, C["gray"], 1.5)
arrow(7.75, 2.5, 8.55, 1.9, C["gray"], 1.5)
arrow(4.75, 0.95, 8.35, 1.0, C["gray"], 3)
ax.text(9.45, 2.95, "한 일도\n결국 열", ha="center", va="center", fontsize=8, color=C["gray"])
save(fig, __file__)
