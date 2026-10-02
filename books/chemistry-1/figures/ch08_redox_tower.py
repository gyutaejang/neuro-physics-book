from figstyle import plt, np, save, C

# 생화학 표준 환원 전위 E°' (pH 7, 25 °C). 위(음수)일수록 전자를 잘 내주고, 아래(양수)일수록 잘 받는다.
pairs = [
    (-0.414, r"2H$^+$ / H$_2$", C["gray"]),
    (-0.320, r"NAD$^+$ / NADH", C["blue"]),
    (-0.219, r"FAD / FADH$_2$ (자유 상태)", C["blue"]),
    (0.045, r"유비퀴논 / 유비퀴놀 (Q / QH$_2$)", C["blue"]),
    (0.254, r"사이토크롬 c (Fe$^{3+}$ / Fe$^{2+}$)", C["blue"]),
    (0.816, r"½O$_2$ / H$_2$O", C["red"]),
]
fig, ax = plt.subplots(figsize=(6.6, 3.9))
for e, lab, col in pairs:
    ax.plot([0, 1], [e, e], color=col, lw=2.2)
    ax.text(1.06, e, f"{lab}   {e:+.3f} V".replace("-", "−"), va="center", fontsize=8.5, color=col)
ax.annotate("", xy=(-0.55, 0.80), xytext=(-0.55, -0.31),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=2, mutation_scale=16))
ax.text(-0.66, 0.25, "전자가 흐르는 방향 (내리막)", ha="center", va="center", fontsize=8.5,
        color=C["red"], rotation=90)
ax.annotate("", xy=(-1.0, 0.816), xytext=(-1.0, -0.320),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.9))
ax.text(-1.08, 0.25, "ΔE°′ = 1.14 V\nΔG°′ ≈ −220 kJ/mol\n(NADH 1개, 전자 2개)", ha="right",
        va="center", fontsize=8.5)
ax.text(0.15, -0.52, "전자를 잘 내준다 (강한 환원제)", ha="left", va="center", fontsize=8.5, color=C["gray"])
ax.text(0.15, 0.92, "전자를 잘 받는다 (강한 산화제)", ha="left", va="center", fontsize=8.5, color=C["gray"])
ax.set_ylim(1.0, -0.58)
ax.set_xlim(-2.5, 3.1)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_position(("data", 0))
ax.spines["left"].set_visible(False)
ax.set_yticks([])
# 눈금 축을 오른쪽 이름과 겹치지 않게 막대 왼쪽에 따로 그린다.
for v in (-0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8):
    ax.plot([-0.05, 0], [v, v], color=C["gray"], lw=0.8)
    ax.text(-0.08, v, f"{v:+.1f}".replace("-", "−").replace("+0.0", "0"), ha="right", va="center",
            fontsize=7.5, color=C["gray"])
ax.plot([0, 0], [-0.45, 0.85], color=C["gray"], lw=0.8)
ax.text(-0.08, -0.52, "E°′ (V)", ha="right", va="bottom", fontsize=8.5, color=C["gray"])
save(fig, __file__)
