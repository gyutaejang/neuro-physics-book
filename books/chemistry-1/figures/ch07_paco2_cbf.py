from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
P = np.linspace(15, 85, 300)

# 왼쪽: HCO3- 24 mM 고정일 때 pH
pH = 6.1 + np.log10(24 / (0.03 * P))
a1.plot(P, pH, color=C["blue"], lw=2)
a1.axhspan(7.35, 7.45, color=C["green"], alpha=0.18, lw=0)
a1.text(84, 7.47, "정상 7.35–7.45", ha="right", va="bottom", fontsize=8, color=C["green"])
for p, lab, off in ((25, "과호흡\n25 mmHg", (8, 8)), (40, "정상\n40 mmHg", (8, 6)), (60, "저호흡\n60 mmHg", (-6, -26))):
    v = 6.1 + np.log10(24 / (0.03 * p))
    a1.scatter([p], [v], color=C["red"], s=20, zorder=5)
    a1.annotate(f"{lab}\npH {v:.2f}", xy=(p, v), xytext=off, textcoords="offset points", fontsize=7.5,
                ha="left" if off[0] > 0 else "right")
a1.set_xlabel("PaCO₂ (mmHg)")
a1.set_ylabel("동맥혈 pH")
a1.set_title("HCO₃⁻ 24 mM으로 고정할 때", fontsize=9.5)
a1.set_xlim(15, 85)
a1.set_ylim(6.85, 7.85)

# 오른쪽: 뇌혈류 (예시 곡선)
L, U, P0, s = 15, 120, 49.2, 13.3
cbf = L + (U - L) / (1 + np.exp(-(P - P0) / s))
a2.plot(P, cbf, color=C["blue"], lw=2)
a2.axhline(50, color=C["gray"], lw=0.6, ls=":")
a2.axvline(40, color=C["gray"], lw=0.6, ls=":")
f = lambda p: L + (U - L) / (1 + np.exp(-(p - P0) / s))
a2.scatter([40], [50], color=C["ink"], s=18, zorder=5)
a2.annotate("기울기 약 3–4% / mmHg", xy=(40, 50), xytext=(42, 33), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.7))
a2.scatter([25], [f(25)], color=C["red"], s=20, zorder=5)
a2.annotate(f"과호흡: 약 −{100 * (1 - f(25) / 50):.0f}%", xy=(25, f(25)), xytext=(16, 60), fontsize=8,
            color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.7))
a2.scatter([50], [f(50)], color=C["purple"], s=20, zorder=5)
a2.annotate(f"CO₂ 흡입 (+10 mmHg):\n약 +{100 * (f(50) / 50 - 1):.0f}%", xy=(50, f(50)), xytext=(57, 50), fontsize=8,
            color=C["purple"], ha="left", arrowprops=dict(arrowstyle="->", color=C["purple"], lw=0.7))
a2.set_xlabel("PaCO₂ (mmHg)")
a2.set_ylabel("뇌혈류 (mL/100 g/분)")
a2.set_title("뇌혈류 (예시 곡선, 개인차 큼)", fontsize=9.5)
a2.set_xlim(15, 85)
a2.set_ylim(0, 130)
fig.tight_layout()
save(fig, __file__)
