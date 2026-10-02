from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0))

# 왼쪽: 경쟁자가 있으면 곡선이 오른쪽으로 평행 이동
L = np.logspace(-2, 3, 400)  # [L]/Kd
for r, col in ((0, C["blue"]), (9, C["purple"]), (99, C["red"])):
    theta = L / (L + (1 + r)) * 100
    a1.semilogx(L, theta, color=col, lw=1.5, label=f"[I]/$K_i$ = {r}")
a1.axhline(50, color=C["gray"], lw=0.5, ls=":")
a1.annotate("", xy=(100, 50), xytext=(1, 50),
            arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=1.0))
for x, lab in ((10, "×10"), (100, "×100")):
    a1.text(x * 1.25, 46, lab, ha="left", va="top", fontsize=8, color=C["gray"])
a1.set_xlabel("[L] / $K_d$ (로그 눈금)")
a1.set_ylabel("L의 점유율 (%)")
a1.set_title("경쟁자가 곡선을 오른쪽으로 민다")
a1.set_xticks([0.01, 1, 100])
a1.set_xticklabels(["1/100", "1", "100"])
a1.minorticks_off()
a1.legend(fontsize=7.5, loc="upper left")
a1.set_ylim(0, 110)

# 오른쪽: 치환 곡선. 추적자 결합이 경쟁자 농도에 따라 줄어든다
I = np.logspace(-2, 3, 400)  # [I]/Ki, 추적자 농도는 Kd보다 훨씬 낮다고 가정
spec = 1 / (1 + I) * 100
a2.semilogx(I, spec, color=C["blue"], lw=1.6)
a2.axhline(50, color=C["gray"], lw=0.5, ls=":")
a2.scatter([1], [50], color=C["red"], s=22, zorder=4)
a2.annotate("IC50 ≈ $K_i$\n(추적자 농도 ≪ $K_d$일 때)", xy=(1, 50), xytext=(3, 68), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.set_xlabel("경쟁자 농도 [I] / $K_i$ (로그 눈금)")
a2.set_ylabel("남은 추적자 특이 결합 (%)")
a2.set_title("치환 곡선")
a2.set_xticks([0.01, 1, 100])
a2.set_xticklabels(["1/100", "1", "100"])
a2.minorticks_off()
a2.set_ylim(0, 110)
fig.tight_layout()
save(fig, __file__)
