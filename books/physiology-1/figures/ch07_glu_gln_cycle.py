import re

from matplotlib.patches import FancyBboxPatch

from figstyle import plt, save, C

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")


def m(t):
    t = re.sub("[₀-₉]+", lambda g: "$_{" + g.group().translate(SUB) + "}$", t)
    return re.sub("[⁰-⁹⁺⁻]+", lambda g: "$^{" + g.group().translate(SUP) + "}$", t)


fig, ax = plt.subplots(figsize=(7.2, 3.9))
ax.set_xlim(0, 10.4)
ax.set_ylim(0, 5.6)
ax.axis("off")

# 시냅스 앞 말단(왼쪽 위), 시냅스 뒤(왼쪽 아래), 성상세포(오른쪽)
ax.add_patch(FancyBboxPatch((0.2, 3.25), 4.1, 2.1, boxstyle="round,pad=0.02,rounding_size=0.3",
                            fc=C["green"], alpha=0.10, ec=C["green"], lw=1.1))
ax.text(0.4, 5.05, "시냅스 앞 말단 (뉴런)", ha="left", fontsize=9, color=C["green"])
ax.add_patch(FancyBboxPatch((0.2, 0.2), 4.1, 1.55, boxstyle="round,pad=0.02,rounding_size=0.3",
                            fc=C["green"], alpha=0.10, ec=C["green"], lw=1.1))
ax.text(0.4, 0.4, "시냅스 뒤 뉴런", ha="left", fontsize=9, color=C["green"])
ax.add_patch(FancyBboxPatch((5.6, 0.2), 4.6, 5.15, boxstyle="round,pad=0.02,rounding_size=0.3",
                            fc=C["purple"], alpha=0.08, ec=C["purple"], lw=1.1))
ax.text(10.0, 5.05, "성상세포", ha="right", fontsize=9, color=C["purple"])
ax.text(0.95, 2.5, "시냅스 틈", ha="center", va="center", fontsize=8.5, color=C["gray"])


def arrow(x0, y0, x1, y1, col, ls="-", rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5, ls=ls, mutation_scale=12,
                                connectionstyle=f"arc3,rad={rad}"))


def label(x, y, t, col=C["ink"], fs=8.3, **kw):
    ax.text(x, y, m(t), ha=kw.pop("ha", "center"), va=kw.pop("va", "center"), fontsize=fs, color=col, **kw)


# 글루탐산 방출과 작용
label(1.6, 4.25, "글루탐산 (소포)", C["blue"])
label(2.2, 4.65, "글루타미나아제로 글루탐산 재생", C["purple"], fs=7.6)
arrow(1.6, 3.95, 1.6, 2.75, C["blue"])
label(1.72, 2.12, "AMPA·NMDA 수용체", C["blue"], fs=7.8, ha="left")
arrow(1.6, 2.4, 1.6, 1.85, C["blue"])
label(2.25, 1.15, "Na⁺ 유입 → Na⁺/K⁺ 펌프\n(뇌 ATP의 가장 큰 몫)", C["red"], fs=8)

# 성상세포 흡수 → 글루타민 → 뉴런으로
arrow(2.2, 2.6, 6.0, 2.6, C["blue"])
label(4.4, 2.78, "EAAT1·2", C["blue"], fs=7.8, va="bottom")
label(7.95, 2.6, "글루탐산 1 + Na⁺ 3 유입 → 펌프 ATP 1", C["blue"], fs=8)
arrow(7.95, 2.85, 7.95, 3.25, C["gray"])
label(7.95, 3.5, "글루타민 합성효소 (ATP 1)", C["red"])
arrow(7.95, 3.75, 7.95, 4.15, C["gray"])
label(7.95, 4.4, "글루타민", C["purple"])
arrow(7.3, 4.4, 4.0, 4.4, C["purple"])
label(5.0, 4.55, "글루타민", C["purple"], fs=8, va="bottom")

# 해당 작용과 젖산(가설)
label(7.95, 1.45, "포도당 1 → 해당 작용 → ATP 2", C["ink"])
label(7.95, 0.95, "+ 젖산 2", C["gray"])
arrow(7.35, 0.95, 4.45, 1.0, C["gray"], ls="--")
label(5.0, 0.72, "젖산 셔틀 (가설)", C["gray"], fs=7.8)
save(fig, __file__)
