from figstyle import plt, np, save, C

f = 26.73  # kT/e (mV), 37 °C
clo = 115.0
fig, ax = plt.subplots(figsize=(5.8, 2.9))
ci = np.logspace(np.log10(2), np.log10(60), 200)
E = -f * np.log(clo / ci)
ax.semilogx(ci, E, color=C["green"], lw=1.8, label="Cl⁻ 평형 전위 (바깥 115 mM)")
ax.axhspan(-75, -65, color=C["gray"], alpha=0.15, lw=0)
ax.text(2.1, -63.5, "성숙 뉴런의 휴지 막전위 부근", fontsize=8, color=C["gray"], va="bottom")
ax.axhline(-55, color=C["red"], lw=0.8, ls="--")
ax.text(59, -54, "활동전위 문턱 약 −55 mV", fontsize=8, color=C["red"], ha="right", va="bottom")

for c, lab, col, off, ha in ((7, "성숙 뉴런\nKCC2 우세\n[Cl⁻]안 ≈ 7 mM", C["blue"], (-14, -18), "right"),
                             (25, "미성숙 뉴런\nNKCC1 우세\n[Cl⁻]안 ≈ 25 mM", C["purple"], (-14, 62), "right")):
    e = -f * np.log(clo / c)
    ax.plot([c], [e], "o", color=col, ms=6, zorder=4)
    eff = "GABA가 열면 탈분극" if c > 10 else "GABA가 열면 과분극"
    ax.annotate(f"{lab}\n" + f"E ≈ {e:.0f} mV".replace("-", "−") + f"\n→ {eff}", xy=(c, e), xytext=off,
                textcoords="offset points", fontsize=8, ha=ha, va="top", color=col,
                arrowprops=dict(arrowstyle="-", color=col, lw=0.6))

ax.set_xlabel("세포 안 Cl⁻ 농도 (mM, 로그 눈금)")
ax.set_ylabel("Cl⁻ 평형 전위 (mV)")
ax.set_xticks([2, 5, 10, 20, 50])
ax.set_xticklabels(["2", "5", "10", "20", "50"])
ax.minorticks_off()
ax.set_ylim(-115, -5)
ax.set_yticks([-100, -80, -60, -40, -20])
ax.set_yticklabels(["−100", "−80", "−60", "−40", "−20"])
ax.set_xlim(2, 60)
ax.legend(fontsize=8, loc="lower right")
save(fig, __file__)
