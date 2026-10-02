import re

from matplotlib.patches import FancyBboxPatch

from figstyle import plt, np, save, C

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")


def m(t):
    # 유니코드 아래·위 첨자는 CJK 글꼴에서 너무 작게 나오므로 mathtext로 바꾼다.
    t = re.sub("[₀-₉]+", lambda g: "$_{" + g.group().translate(SUB) + "}$", t)
    return re.sub("[⁰-⁹⁺⁻]+", lambda g: "$^{" + g.group().translate(SUP) + "}$", t)


fig, ax = plt.subplots(figsize=(7.4, 3.5))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5)
ax.axis("off")

species = [
    (0.7, "O₂", "산소", "0", C["blue"]),
    (3.0, "O₂•⁻", "슈퍼옥사이드", "−½", C["red"]),
    (5.3, "H₂O₂", "과산화수소", "−1", C["red"]),
    (7.5, "•OH", "하이드록실 라디칼", "−1", C["red"]),
    (9.8, "H₂O", "물", "−2", C["blue"]),
]
y = 2.9
for x, f, name, ox, col in species:
    w = 1.15 if f != "H₂O" else 0.8
    ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.38), w, 0.76, boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="white", edgecolor=col, lw=1.5))
    ax.text(x, y, m(f).replace("•", r"$\bullet$"), ha="center", va="center", fontsize=11, color=col)
    ax.text(x, y - 0.6, name, ha="center", va="top", fontsize=8.3)
    ax.text(x, y - 1.0, f"O의 산화수 {ox}", ha="center", va="top", fontsize=8, color=C["gray"])

steps = [(0.7, 3.0, "+e⁻"), (3.0, 5.3, "+e⁻ +2H⁺"), (5.3, 7.5, "+e⁻"), (7.5, 9.8, "+e⁻ +H⁺")]
for x0, x1, lab in steps:
    ax.annotate("", xy=(x1 - 0.62, y), xytext=(x0 + 0.62, y),
                arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.2, mutation_scale=11))
    ax.text((x0 + x1) / 2, y + 0.12, m(lab), ha="center", va="bottom", fontsize=8.3)
ax.text(6.4, y + 0.5, m("펜톤 반응: Fe²⁺가 전자를 준다"), ha="center", va="bottom", fontsize=8.3,
        color=C["red"])

# 방어: SOD, 카탈레이스/GPx
ax.annotate("", xy=(5.3, 1.35), xytext=(3.0, 1.35),
            arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.6, mutation_scale=12))
ax.text(4.15, 1.2, "SOD (슈퍼옥사이드\n불균등화효소)", ha="center", va="top", fontsize=8.3, color=C["green"])
ax.annotate("", xy=(9.8, 1.45), xytext=(5.4, 1.45),
            arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.6, mutation_scale=12,
                            connectionstyle="arc3,rad=0.22"))
ax.text(7.6, 0.85, "카탈레이스, 글루타티온\n과산화효소(GPx)", ha="center", va="top", fontsize=8.3,
        color=C["green"])
ax.text(7.5, 4.2, "막는 효소가 없다:\n가까운 지질·DNA·단백질을 공격", ha="center", va="bottom", fontsize=8.3,
        color=C["red"])
ax.text(0.05, 0.12, m("정상 경로: O₂ + 4e⁻ + 4H⁺ → 2H₂O를 사이토크롬 산화효소(복합체 IV)가 한 번에 처리"),
        ha="left", va="center", fontsize=8.5, color=C["blue"])
save(fig, __file__)
