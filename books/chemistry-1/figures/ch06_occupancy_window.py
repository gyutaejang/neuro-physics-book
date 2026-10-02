from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1]))

# 왼쪽: 혈장 농도 대 D2 점유율 (가상의 약물, C50 = 1)
c = np.linspace(0, 10, 400)
occ = c / (c + 1) * 100
a1.axhspan(65, 80, color=C["green"], alpha=0.18, lw=0)
a1.text(9.8, 72.5, "치료 창 약 65–80 %", ha="right", va="center", fontsize=8.5, color=C["green"])
a1.text(9.8, 93.5, "80 % 이상: 추체외로 부작용 위험 증가", ha="right", va="bottom", fontsize=7.5, color=C["red"])
a1.plot(c, occ, color=C["blue"], lw=1.6)
for x in (1, 2, 4):
    y = x / (x + 1) * 100
    a1.scatter([x], [y], color=C["red"], s=22, zorder=4)
    a1.annotate(f"{y:.0f} %", xy=(x, y), xytext=(4, -12), textcoords="offset points", fontsize=8)
a1.set_xlabel("혈장 농도 ($C_{50}$의 배수)")
a1.set_ylabel("D2 점유율 (%)")
a1.set_title("농도 2배 → 점유율 67 → 80 %")
a1.set_ylim(0, 105)

# 오른쪽: PET로 점유율 재기 (BP 막대)
bars = [("약 없음", 3.0, C["blue"]), ("약 복용", 0.9, C["purple"])]
for i, (lab, bp, col) in enumerate(bars):
    a2.bar(i, bp, width=0.55, color=col, alpha=0.85)
    a2.text(i, bp + 0.08, f"BP$_{{ND}}$ = {bp}", ha="center", va="bottom", fontsize=8.5)
a2.set_xticks([0, 1])
a2.set_xticklabels([b[0] for b in bars])
a2.set_ylabel("[¹¹C]라클로프라이드 BP$_{ND}$")
a2.set_ylim(0, 3.8)
a2.annotate("", xy=(1.42, 0.92), xytext=(1.42, 2.98),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.2))
a2.plot([0.27, 1.42], [3.0, 3.0], color=C["gray"], lw=0.6, ls=":")
a2.plot([1.27, 1.42], [0.9, 0.9], color=C["gray"], lw=0.6, ls=":")
a2.text(1.52, 1.95, "점유율\n= 1 − 0.9/3.0\n= 70 %", fontsize=8.5, va="center")
a2.set_xlim(-0.5, 2.45)
a2.set_title("PET에서 점유율 구하기")
fig.tight_layout()
save(fig, __file__)
