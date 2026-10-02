from matplotlib.patches import FancyBboxPatch
from figstyle import plt, save, C

fig, ax = plt.subplots(figsize=(7.2, 3.1))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.0)
ax.axis("off")


def box(x, y, w, h, text, col, fs=9.5, alpha=0.12):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                facecolor=col, alpha=alpha, edgecolor="none"))
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                facecolor="none", edgecolor=col, lw=1))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=C["ink"])


def eq_arrow(x1, x2, y, label=None, col=C["ink"]):
    ax.annotate("", xy=(x2, y + 0.07), xytext=(x1, y + 0.07),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.1, mutation_scale=10))
    ax.annotate("", xy=(x1, y - 0.07), xytext=(x2, y - 0.07),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.1, mutation_scale=10))
    if label:
        ax.text((x1 + x2) / 2, y + 0.6, label, ha="center", va="bottom", fontsize=7.5, color=C["purple"])


y0 = 3.2
box(0.85, y0, 1.4, 0.9, "폐\nCO₂ 배출", C["gray"])
box(2.8, y0, 1.6, 0.9, "CO₂ (녹은 것)\n+ H₂O", C["blue"])
box(5.4, y0, 1.2, 0.9, "H₂CO₃\n(탄산)", C["blue"])
box(8.3, y0, 2.4, 0.9, "H⁺  +  HCO₃⁻\n(중탄산 이온)", C["blue"])
eq_arrow(1.6, 1.95, y0)
eq_arrow(3.65, 4.75, y0, "탄산탈수효소")
eq_arrow(6.05, 7.05, y0)

# 아래: 숫자
ax.text(2.8, 2.45, "PaCO₂ 40 mmHg × 0.03\n= 1.2 mM", ha="center", va="top", fontsize=8.5, color=C["blue"])
ax.text(8.85, 2.45, "HCO₃⁻ 24 mM", ha="center", va="top", fontsize=8.5, color=C["blue"])
ax.text(7.55, 2.45, "H⁺ 40 nM", ha="center", va="top", fontsize=8.5, color=C["red"])
ax.text(4.4, 1.45, "pH = 6.1 + log(24 / 1.2) = 6.1 + log 20 = 7.40", ha="center", va="center", fontsize=10,
        bbox=dict(facecolor="white", edgecolor=C["gray"], boxstyle="round,pad=0.35", lw=0.8))
ax.text(0.85, 2.45, "호흡이\n분모를 정한다\n(분~초)", ha="center", va="top", fontsize=8, color=C["gray"])
ax.text(8.3, 2.0, "콩팥이 HCO₃⁻를 조절하고\nH⁺를 내보낸다 (시간~일)", ha="center", va="top",
        fontsize=8, color=C["gray"])
ax.text(5.0, 0.35, "혈액뇌장벽: CO₂는 몇 초 만에 지나가지만 HCO₃⁻와 H⁺는 거의 못 지나간다",
        ha="center", va="center", fontsize=8.5, color=C["green"])
save(fig, __file__)
