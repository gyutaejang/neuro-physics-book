from figstyle import plt, np, save, C

P = np.linspace(0, 120, 500)
hill = lambda p, p50, n: p ** n / (p ** n + p50 ** n) * 100

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.4))

# 왼쪽: 미오글로빈 대 헤모글로빈
a1.plot(P, hill(P, 2.8, 1), color=C["purple"], lw=1.4, label="미오글로빈 (P50 약 3)")
a1.plot(P, hill(P, 26.8, 2.7), color=C["red"], lw=1.8, label="헤모글로빈 (P50 약 27)")
a1.plot(P, hill(P, 26.8, 1), color=C["gray"], lw=1.0, ls="--", label="P50이 같고 협동성이 없다면")
for p, lab, xy, ha in ((100, "동맥 100 mmHg, 97 %", (104, 86), "right"), (40, "정맥 40 mmHg\n75 %", (52, 50), "left")):
    s = hill(p, 26.8, 2.7)
    a1.scatter([p], [s], color=C["red"], s=24, zorder=4)
    a1.annotate(lab, xy=(p, s), xytext=xy, fontsize=8, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a1.axhline(50, color=C["gray"], lw=0.5, ls=":")
a1.set_xlabel("산소 분압 PO₂ (mmHg)")
a1.set_ylabel("산소 포화도 (%)")
a1.set_title("협동 결합이 S자를 만든다")
a1.set_ylim(0, 105)
a1.set_xlim(0, 122)
a1.legend(fontsize=7.3, loc="lower right")

# 오른쪽: 곡선의 이동 (보어 효과, 온도, 2,3-BPG)
for p50, col, lab in ((20, C["blue"], "왼쪽 이동 (P50 약 20)"),
                      (26.8, C["red"], "정상 (P50 약 27)"),
                      (33.4, C["purple"], "오른쪽 이동 (P50 약 33)")):
    a2.plot(P, hill(P, p50, 2.7), color=col, lw=1.5, label=lab)
a2.text(119, 46, "오른쪽: pH↓, CO₂↑, 체온↑, 2,3-BPG↑", ha="right", fontsize=7.5, color=C["purple"])
a2.text(119, 37, "왼쪽: pH↑, CO₂↓, 체온↓", ha="right", fontsize=7.5, color=C["blue"])
a2.axvline(40, color=C["gray"], lw=0.6, ls=":")
a2.text(38, 4, "조직\n40 mmHg", fontsize=7.5, color=C["gray"], ha="right")
a2.set_xlabel("산소 분압 PO₂ (mmHg)")
a2.set_title("곡선의 이동")
a2.set_ylim(0, 105)
a2.set_xlim(0, 122)
a2.legend(fontsize=7.3, loc="lower right")
fig.tight_layout()
save(fig, __file__)
