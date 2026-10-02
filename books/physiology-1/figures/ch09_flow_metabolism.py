from figstyle import plt, np, save, C

# CBF와 CMRO2 변화 → OEF → 정맥 포화도 → BOLD (데이비스 모형).
Ya, OEF0 = 0.98, 0.40
M, alpha, beta = 0.08, 0.2, 1.3
f = np.linspace(1.0, 1.8, 200)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.3))
for r, col, lab in ((1.0, C["gray"], "CMRO$_2$ 변화 없음"), (1.1, C["blue"], "CMRO$_2$ +10%"),
                    (1.2, C["red"], "CMRO$_2$ +20%")):
    oef = OEF0 * r / f
    a1.plot((f - 1) * 100, Ya * (1 - oef) * 100, color=col, lw=1.7, label=lab)
    bold = M * (1 - f ** (alpha - beta) * r ** beta) * 100
    a2.plot((f - 1) * 100, bold, color=col, lw=1.7, label=lab)

# 예제 점: CBF +50%, CMRO2 +20%
yv = Ya * (1 - OEF0 * 1.2 / 1.5) * 100
b = M * (1 - 1.5 ** (alpha - beta) * 1.2 ** beta) * 100
a1.scatter([50], [yv], color=C["red"], s=26, zorder=4)
a1.annotate(f"약 {yv:.0f}%", xy=(50, yv), xytext=(56, yv - 6), fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a1.scatter([0], [Ya * (1 - OEF0) * 100], color=C["ink"], s=22, zorder=4)
a1.annotate("휴지 약 59%", xy=(0, Ya * (1 - OEF0) * 100), xytext=(22, 52), fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a1.set_xlabel("CBF 증가 (%)")
a1.set_ylabel("정맥 산소 포화도 (%)")
a1.set_title("공급이 수요보다 크면 정맥이 붉어진다", fontsize=9.5)
a1.set_ylim(50, 80)
a1.legend(fontsize=7.8, loc="upper left")

a2.axhline(0, color=C["gray"], lw=0.6)
a2.scatter([50], [b], color=C["red"], s=26, zorder=4)
a2.annotate(f"약 {b:.1f}%  (n = 2.5)", xy=(50, b), xytext=(48, 0.2), fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.set_xlabel("CBF 증가 (%)")
a2.set_ylabel("BOLD 신호 변화 (%)")
a2.set_title("데이비스 모형 (M = 8%, 3 T)", fontsize=9.5)
a2.set_ylim(-1.2, 4.2)
fig.tight_layout()
save(fig, __file__)
