import re

from matplotlib.patches import FancyBboxPatch, Ellipse

from figstyle import plt, np, save, C

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")


def m(t):
    # 유니코드 아래·위 첨자는 CJK 글꼴에서 너무 작게 나오므로 mathtext로 바꾼다.
    t = re.sub("[₀-₉]+", lambda g: "$_{" + g.group().translate(SUB) + "}$", t)
    return re.sub("[⁰-⁹⁺⁻]+", lambda g: "$^{" + g.group().translate(SUP) + "}$", t)


fig, ax = plt.subplots(figsize=(7.4, 4.0))
ax.set_xlim(0, 10.6)
ax.set_ylim(-0.7, 6.0)
ax.axis("off")

# 내막 (y 2.2–3.2)
ax.add_patch(plt.Rectangle((0, 2.2), 10.6, 1.0, color=C["green"], alpha=0.15, lw=0))
ax.text(0.1, 5.7, m("막사이 공간: H⁺ 많음, 양(+)"), fontsize=9, color=C["ink"], va="center")
ax.text(0.1, -0.45, m("기질(matrix): H⁺ 적음, 음(−)"), fontsize=9, color=C["ink"], va="center")
ax.text(10.5, 2.7, "내막", fontsize=8.5, color=C["green"], ha="right", va="center")


def cpx(x, w, name, col=C["blue"]):
    ax.add_patch(FancyBboxPatch((x, 1.75), w, 1.9, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor="white", edgecolor=col, lw=1.5))
    ax.text(x + w / 2, 2.7, name, ha="center", va="center", fontsize=9.5, weight="bold", color=col)


cpx(0.6, 1.2, "I")
cpx(2.25, 0.9, "II")
cpx(4.3, 1.1, "III")
cpx(6.3, 1.1, "IV")
# Q와 사이토크롬 c
ax.add_patch(Ellipse((3.65, 2.7), 0.55, 0.45, facecolor=C["light"], edgecolor=C["blue"]))
ax.text(3.65, 2.7, "Q", ha="center", va="center", fontsize=9, color=C["blue"])
ax.add_patch(Ellipse((5.85, 4.05), 0.6, 0.45, facecolor=C["light"], edgecolor=C["blue"]))
ax.text(5.85, 4.05, "c", ha="center", va="center", fontsize=9, color=C["blue"])
# ATP 합성효소
ax.add_patch(FancyBboxPatch((8.45, 1.9), 0.75, 1.6, boxstyle="round,pad=0.02,rounding_size=0.2",
                            facecolor="white", edgecolor=C["red"], lw=1.5))
ax.add_patch(Ellipse((8.82, 1.25), 1.3, 0.9, facecolor="white", edgecolor=C["red"], lw=1.5))
ax.text(8.82, 1.25, "ATP\n합성효소", ha="center", va="center", fontsize=7.5, color=C["red"])

# 전자의 길 (점선)
path = [(1.2, 2.0), (3.65, 2.5), (4.85, 2.4), (5.85, 3.85), (6.85, 2.4)]
xs, ys = zip(*path)
ax.plot(xs, ys, ls="--", color=C["purple"], lw=1.4)
ax.annotate("", xy=(6.85, 2.2), xytext=(6.85, 2.4),
            arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.4, mutation_scale=10))
ax.text(5.85, 4.45, m("e⁻의 길"), fontsize=8.5, color=C["purple"], ha="center", va="bottom")

# 기질 쪽 반응
ax.annotate("", xy=(1.2, 1.75), xytext=(1.2, 0.85),
            arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1))
ax.text(1.2, 0.65, m("NADH → NAD⁺"), fontsize=8.5, ha="center", va="top")
ax.annotate("", xy=(2.7, 1.75), xytext=(2.7, 0.85),
            arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1))
ax.text(2.85, 0.65, "숙신산\n→ 푸마르산",
        fontsize=8, ha="center", va="top")
ax.annotate("", xy=(6.85, 0.85), xytext=(6.85, 1.75),
            arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1))
ax.text(6.85, 0.65, m("½O₂ + 2H⁺ → H₂O"), fontsize=8.5, ha="center", va="top", color=C["red"])
ax.text(8.82, 0.55, m("ADP + Pᵢ → ATP").replace("Pᵢ", r"P$_\mathrm{i}$"), fontsize=8.5,
        ha="center", va="top", color=C["red"])

# 양성자 펌프 (위로)
for x, n in ((1.2, 4), (4.85, 4), (6.85, 2)):
    ax.annotate("", xy=(x, 4.85), xytext=(x, 3.65),
                arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.8, mutation_scale=12))
    ax.text(x + 0.12, 5.0, m(f"{n}H⁺"), fontsize=9, color=C["green"], ha="center", va="bottom")
# 양성자가 ATP 합성효소로 돌아온다 (아래로)
ax.annotate("", xy=(8.82, 1.85), xytext=(8.82, 4.85),
            arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.8, mutation_scale=12))
ax.text(8.95, 5.0, m("H⁺ 약 2.7–4개 / ATP"), fontsize=8.5, color=C["green"], ha="left", va="bottom")
ax.text(9.6, 3.9, "Δp ≈\n0.15–0.2 V", fontsize=8.5, color=C["ink"], ha="center", va="center")
save(fig, __file__)
