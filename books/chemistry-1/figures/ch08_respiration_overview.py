from matplotlib.patches import FancyBboxPatch

from figstyle import plt, np, save, C
import re

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")


def m(t):
    # 유니코드 아래·위 첨자는 CJK 글꼴에서 너무 작게 나오므로 mathtext로 바꾼다.
    t = re.sub("[₀-₉]+", lambda g: "$_{" + g.group().translate(SUB) + "}$", t)
    return re.sub("[⁰-⁹⁺⁻]+", lambda g: "$^{" + g.group().translate(SUP) + "}$", t)



fig, ax = plt.subplots(figsize=(7.4, 3.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")

# 세포질과 미토콘드리아 영역
ax.add_patch(FancyBboxPatch((3.0, 0.15), 6.85, 4.55, boxstyle="round,pad=0.02,rounding_size=0.4",
                            facecolor=C["green"], alpha=0.07, edgecolor=C["green"], lw=1))
ax.text(9.7, 4.5, "미토콘드리아", ha="right", va="center", fontsize=9, color=C["green"])
ax.text(0.15, 4.9, "세포질", ha="left", va="center", fontsize=9, color=C["gray"])


def box(x, y, w, h, title, lines, col):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="white", edgecolor=col, lw=1.4))
    ax.text(x + w / 2, y + h - 0.25, title, ha="center", va="top", fontsize=9.5, weight="bold", color=col)
    ax.text(x + w / 2, y + h - 0.75, m(lines), ha="center", va="top", fontsize=8.3, linespacing=1.45)


box(0.15, 1.6, 2.5, 2.7, "① 해당 작용", "포도당 (C 6개)\n→ 피루브산 2\n\nATP 2\nNADH 2", C["blue"])
box(3.3, 1.6, 2.7, 2.7, "② 피루브산 산화\n+ TCA 회로", "\n피루브산 2 → CO₂ 6\n\nNADH 8, FADH₂ 2\nGTP(ATP) 2", C["blue"])
box(6.6, 1.6, 3.05, 2.7, "③ 전자전달계\n+ ATP 합성효소", "\nNADH 10 + FADH₂ 2\n= 전자 24개\n6 O₂ + 24 e⁻ + 24 H⁺\n→ 12 H₂O", C["red"])
for x0, x1 in ((2.65, 3.3), (6.0, 6.6)):
    ax.annotate("", xy=(x1, 2.95), xytext=(x0, 2.95),
                arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.4, mutation_scale=12))
ax.text(4.65, 1.3, m("탄소는 여기서 CO₂로 떠난다"), ha="center", va="top", fontsize=8.3, color=C["gray"])
ax.text(8.12, 1.3, "산소는 여기서만 쓰인다", ha="center", va="top", fontsize=8.3, color=C["red"])
ax.text(8.12, 0.75, "양성자 기울기 → ATP 약 26–28", ha="center", va="top", fontsize=8.5, color=C["red"])
ax.text(1.4, 1.3, "산소 없이도 진행", ha="center", va="top", fontsize=8.3, color=C["gray"])
ax.text(5.0, 5.05, "포도당 1개당 ATP 합계: 약 30–32", ha="center", va="center", fontsize=10,
        weight="bold", color=C["ink"])
save(fig, __file__)
