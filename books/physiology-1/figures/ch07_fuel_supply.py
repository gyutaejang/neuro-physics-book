import re

from matplotlib.patches import FancyBboxPatch

from figstyle import plt, save, C

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def m(t):
    # 유니코드 아래 첨자는 CJK 글꼴에서 너무 작게 나오므로 mathtext로 바꾼다.
    return re.sub("[₀-₉]+", lambda g: "$_{" + g.group().translate(SUB) + "}$", t)


fig, ax = plt.subplots(figsize=(7.2, 3.7))
ax.set_xlim(0, 10.4)
ax.set_ylim(0, 5.3)
ax.axis("off")

# 구획: 혈액, 내피, 세포 밖 공간, 성상세포, 뉴런
ax.add_patch(FancyBboxPatch((0.1, 0.3), 1.9, 4.5, boxstyle="round,pad=0.02,rounding_size=0.25",
                            fc=C["red"], alpha=0.10, ec="none"))
ax.text(1.05, 5.0, "모세혈관 혈액", ha="center", fontsize=9.5)
ax.add_patch(plt.Rectangle((2.05, 0.3), 0.35, 4.5, fc=C["gray"], alpha=0.25, ec="none"))
ax.text(2.22, 0.12, "내피(혈액뇌장벽)", ha="center", va="top", fontsize=8, color=C["gray"])
ax.text(3.45, 5.0, "세포 밖 공간", ha="center", fontsize=9.5, color=C["gray"])
ax.add_patch(FancyBboxPatch((5.0, 2.85), 5.25, 1.95, boxstyle="round,pad=0.02,rounding_size=0.25",
                            fc=C["purple"], alpha=0.08, ec=C["purple"], lw=1.1))
ax.text(10.1, 4.55, "성상세포", ha="right", fontsize=9.5, color=C["purple"])
ax.add_patch(FancyBboxPatch((5.0, 0.3), 5.25, 2.15, boxstyle="round,pad=0.02,rounding_size=0.25",
                            fc=C["green"], alpha=0.08, ec=C["green"], lw=1.1))
ax.text(10.1, 0.5, "뉴런", ha="right", fontsize=9.5, color=C["green"])

# 농도 표시
ax.text(1.05, 4.35, "포도당 약 5 mM", ha="center", fontsize=8.5, color=C["blue"])
ax.text(3.45, 4.35, "포도당 약 1–2 mM", ha="center", fontsize=8.5, color=C["blue"])


def arrow(x0, y0, x1, y1, col, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5, ls=ls, mutation_scale=12))


def tag(x, y, t, col):
    ax.text(x, y, m(t), ha="center", va="center", fontsize=7.8, color=col,
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=col, lw=0.9))


# 포도당: 혈액 → 세포 밖 → 성상세포, 뉴런
arrow(1.3, 3.6, 3.0, 3.6, C["blue"])
tag(2.22, 3.6, "GLUT1", C["blue"])
arrow(3.9, 3.85, 5.6, 3.85, C["blue"])
tag(5.0, 3.85, "GLUT1", C["blue"])
ax.text(7.5, 3.85, "포도당 → 해당 작용 → 젖산?", ha="center", va="center", fontsize=8.5)
arrow(3.9, 1.6, 5.6, 1.6, C["blue"])
tag(5.0, 1.6, "GLUT3", C["blue"])
ax.text(7.6, 1.6, "포도당 → 해당 → TCA → ATP", ha="center", va="center", fontsize=8.5)

# 케톤체
arrow(1.3, 2.5, 3.0, 2.5, C["green"])
tag(2.22, 2.5, "MCT1", C["green"])
ax.text(1.05, 2.15, "케톤체\n(단식 시 증가)", ha="center", va="top", fontsize=8, color=C["green"])
ax.text(3.45, 2.5, "케톤체", ha="center", va="center", fontsize=8.3, color=C["green"])
arrow(3.9, 2.25, 5.6, 1.95, C["green"])

# 산소
arrow(1.3, 0.9, 5.6, 0.9, C["red"])
ax.text(3.45, 1.0, m("O₂: 막을 그냥 확산"), ha="center", va="bottom", fontsize=8.3, color=C["red"])
ax.text(1.05, 0.65, m("Hb에서 풀린 O₂"), ha="center", va="top", fontsize=8, color=C["red"])

# 젖산 셔틀(가설)
arrow(7.5, 3.5, 7.5, 2.0, C["gray"], ls="--")
ax.text(7.65, 2.72, "젖산 (MCT4 → MCT2)\n가설, 7.4절", ha="left", va="center", fontsize=7.8, color=C["gray"])
save(fig, __file__)
