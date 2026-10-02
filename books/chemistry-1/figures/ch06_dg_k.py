from figstyle import plt, np, save, C

RT = 8.314e-3 * 310.15  # kJ/mol
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1.1, 1]))

# 왼쪽: ΔG° 대 log10 K
lk = np.linspace(-4, 10, 100)
a1.plot(lk, -RT * np.log(10) * lk, color=C["blue"], lw=1.6)
a1.axhline(0, color=C["gray"], lw=0.6, ls=":")
a1.axvline(0, color=C["gray"], lw=0.6, ls=":")
for x in (1, 9):
    a1.scatter([x], [-RT * np.log(10) * x], color=C["red"], s=24, zorder=4)
a1.annotate("K = 10 → −5.9 kJ/mol", xy=(1, -5.9), xytext=(6, 6), textcoords="offset points", fontsize=8, va="center")
a1.annotate("Kd = 1 nM 결합\n(K = 10⁹) → −53 kJ/mol", xy=(9, -53.4), xytext=(10.3, -16), fontsize=8,
            ha="right", va="center", arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a1.set_xlabel(r"$\log_{10}\,K$")
a1.set_ylabel("ΔG° (kJ/mol)")
a1.set_title("한 자릿수마다 5.9 kJ/mol (37 °C)")
a1.set_yticks([-60, -40, -20, 0, 20])
a1.set_yticklabels(["−60", "−40", "−20", "0", "20"])
a1.set_xticks([-4, -2, 0, 2, 4, 6, 8, 10])
a1.set_xticklabels(["−4", "−2", "0", "2", "4", "6", "8", "10"])
a1.text(-3.8, -58, "← K < 1: 반응물 쪽", fontsize=8, color=C["gray"], va="bottom")
a1.text(10, 17, "K > 1: 생성물 쪽 →", fontsize=8, color=C["gray"], ha="right", va="center")

# 오른쪽: A ⇌ B에서 평형의 B 비율 대 ΔG°
dg = np.linspace(-20, 20, 300)
frac = 1 / (1 + np.exp(dg / RT))
a2.plot(dg, frac * 100, color=C["blue"], lw=1.6)
a2.axvline(0, color=C["gray"], lw=0.6, ls=":")
for d in (-5.9, 5.9):
    f = 1 / (1 + np.exp(d / RT)) * 100
    a2.scatter([d], [f], color=C["red"], s=22, zorder=4)
    a2.annotate(f"{f:.0f} %", xy=(d, f), xytext=(7 if d < 0 else -30, -4 if d < 0 else 8),
                textcoords="offset points", fontsize=8.5)
a2.set_xlabel("ΔG° (kJ/mol)")
a2.set_ylabel("평형에서 B의 비율 (%)")
a2.set_title("A ⇌ B: ±12 kJ/mol이면 거의 한쪽")
a2.set_xticks([-20, -10, 0, 10, 20])
a2.set_xticklabels(["−20", "−10", "0", "10", "20"])
fig.tight_layout()
save(fig, __file__)
