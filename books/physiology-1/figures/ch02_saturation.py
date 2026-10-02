from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.6), gridspec_kw=dict(width_ratios=[1, 1.15]))

# 왼쪽: 단순 확산(직선) 대 운반체(포화)
c = np.linspace(0, 20, 300)
Km, Jmax = 3.0, 1.0
a1.plot(c, Jmax * c / (Km + c), color=C["purple"], lw=1.8, label="운반체 (포화)")
a1.plot(c, 0.06 * c, color=C["ink"], lw=1.4, ls="--", label="단순 확산 (직선)")
a1.axhline(Jmax, color=C["gray"], lw=0.7, ls=":")
a1.text(0.4, Jmax + 0.03, "$J_{max}$", ha="left", va="bottom", fontsize=9, color=C["gray"])
a1.plot([Km, Km], [0, 0.5], color=C["gray"], lw=0.7, ls=":")
a1.plot([0, Km], [0.5, 0.5], color=C["gray"], lw=0.7, ls=":")
a1.text(Km + 0.4, 0.06, "$K_m$", fontsize=9, color=C["gray"])
a1.text(0.3, 0.53, "$J_{max}$/2", fontsize=8, color=C["gray"], va="bottom")
a1.set_xlabel("바깥 농도 (mM)")
a1.set_ylabel("들어오는 흐름 (상대값)")
a1.set_ylim(0, 1.3)
a1.set_xlim(0, 20)
a1.legend(fontsize=8, loc="lower right")
a1.set_title("(가) 운반체는 포화된다", fontsize=10)

# 오른쪽: 단백질 하나가 1초에 옮기는 이온/분자 수
items = [("Na⁺/K⁺ 펌프", 30, 150, C["red"]),
         ("운반체 (GLUT 등)", 1e2, 1e4, C["purple"]),
         ("이온 통로", 1e6, 1e8, C["blue"])]
for k, (name, lo, hi, col) in enumerate(items):
    a2.plot([lo, hi], [k, k], color=col, lw=9, solid_capstyle="butt", alpha=0.8)
    a2.text(lo / 1.6, k, name, ha="right", va="center", fontsize=8.5)
a2.set_xscale("log")
a2.set_xlim(1e-1, 1e9)
a2.set_ylim(-0.7, 2.7)
a2.set_yticks([])
a2.spines["left"].set_visible(False)
a2.set_xticks([1, 1e2, 1e4, 1e6, 1e8])
a2.set_xticklabels(["1", "10²", "10⁴", "10⁶", "10⁸"])
a2.minorticks_off()
a2.set_xlabel("단백질 하나가 1초에 옮기는 수")
a2.set_title("(나) 통로는 운반체보다 수천 배 빠르다", fontsize=10)
fig.tight_layout()
save(fig, __file__)
