from matplotlib.patches import FancyBboxPatch

from figstyle import plt, save, C

# 혈관을 넓히는(또는 좁히는) 주요 신호 경로 도식.
fig, ax = plt.subplots(figsize=(7.3, 4.3))
ax.set_xlim(0, 10)
ax.set_ylim(-0.1, 6.25)
ax.axis("off")


def box(x, y, w, txt, col, dashed=False, fc="white", fs=7.8, h=0.62):
    ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=col, lw=1.1, ls="--" if dashed else "-"))
    ax.text(x + w / 2, y, txt, ha="center", va="center", fontsize=fs, color=C["ink"])


def arrow(x1, x2, y, col=C["gray"], dashed=False):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, mutation_scale=9,
                                ls="--" if dashed else "-"))


for x, t in ((1.05, "신호의 출발점"), (4.15, "매개 물질"), (8.2, "혈관 쪽 표적과 효과")):
    ax.text(x, 6.0, t, ha="center", fontsize=9, color=C["gray"])

G, R, B = C["green"], C["red"], C["blue"]
rows = [
    (5.25, "뉴런: 글루탐산\n→ NMDA → Ca²⁺", "nNOS → NO", "평활근 cGMP↑ → 이완", False, "확장"),
    (4.35, "뉴런: Ca²⁺ → COX-2", "PGE$_2$", "EP4 수용체(평활근·주피세포)", False, "확장"),
    (3.45, "성상세포 Ca²⁺↑\n→ PLA$_2$ → 아라키돈산", "EET / 20-HETE", "평활근 K⁺ 통로 / 수축", True, "확장 또는 수축"),
    (2.55, "활동전위·시냅스\n→ 세포 밖 K⁺↑", "K⁺ (수 mM)", "모세혈관 내피 Kir2.1\n→ 과분극", False, "확장"),
    (1.65, "ATP 소모", "아데노신", "A2A 수용체", False, "확장"),
    (0.75, "억제성 인터뉴런", "NO, VIP / NPY, SST", "평활근", False, "확장 또는 수축"),
]
for y, src, med, tgt, dashed, eff in rows:
    box(0.0, y, 2.1, src, G, dashed, fc="#eef5ec")
    arrow(2.12, 2.95, y)
    box(2.95, y, 2.4, med, B, dashed)
    arrow(5.37, 6.15, y)
    box(6.15, y, 2.55, tgt, C["ink"], dashed)
    ax.text(8.8, y, eff, va="center", fontsize=7.8,
            color=R if eff == "확장" else C["purple"])

ax.text(9.98, 2.15, "→ 상류로 역행 전파", ha="right", va="top", fontsize=7.2, color=R)
ax.text(0.0, 0.1, "점선: 생체 안에서 얼마나 기여하는지가 논쟁 중인 경로. 화살표는 단순화했다.", fontsize=7.4, color=C["gray"], va="center")
save(fig, __file__)
