from figstyle import plt, np, save, C

f = 26.73  # kT/e (mV), 37 °C
Ki, Nao, Nai = 140.0, 145.0, 15.0


def ghk(Ko, r):
    return f * np.log((Ko + r * Nao) / (Ki + r * Nai))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1.2, 1]))

Ko = np.logspace(np.log10(1), np.log10(140), 200)
a1.semilogx(Ko, f * np.log(Ko / Ki), color=C["gray"], lw=1.2, ls="--", label="$E_K$ (네른스트)")
for r, col, lab in ((0.01, C["blue"], "GHK, $P_{Na}/P_K$ = 0.01"), (0.04, C["green"], "GHK, $P_{Na}/P_K$ = 0.04")):
    a1.semilogx(Ko, ghk(Ko, r), color=col, lw=1.8, label=lab)
a1.axvspan(3, 5, color=C["light"], lw=0)
a1.text(3.9, 12, "정상", ha="center", fontsize=8)
a1.axvspan(30, 140, color=C["red"], alpha=0.08, lw=0)
a1.text(64, 12, "확산성\n탈분극", ha="center", fontsize=8, color=C["red"], va="center")
a1.plot([5], [ghk(5, 0.04)], "o", color=C["green"], ms=5, zorder=4)
a1.annotate("−69 mV", xy=(5, ghk(5, 0.04)), xytext=(8, -92), fontsize=8, color=C["green"],
            arrowprops=dict(arrowstyle="-", color=C["green"], lw=0.6))
a1.set_xlabel("세포 밖 K⁺ (mM, 로그 눈금)")
a1.set_ylabel("휴지 막전위 (mV)")
a1.set_xticks([1, 3, 10, 30, 100])
a1.set_xticklabels(["1", "3", "10", "30", "100"])
a1.minorticks_off()
a1.set_ylim(-130, 25)
a1.set_yticks([-120, -90, -60, -30, 0])
a1.set_yticklabels(["−120", "−90", "−60", "−30", "0"])
a1.legend(fontsize=7.5, loc="lower right")
a1.set_title("(가) 바깥 K⁺에 따른 막전위", fontsize=10)

r = np.logspace(-3, 2, 300)
a2.semilogx(r, ghk(5, r), color=C["green"], lw=1.8)
a2.axhline(f * np.log(5 / Ki), color=C["blue"], lw=0.8, ls=":")
a2.axhline(f * np.log(Nao / Nai), color=C["red"], lw=0.8, ls=":")
a2.text(90, -86, "$E_K$ ≈ −89 mV", fontsize=8, color=C["blue"], va="bottom", ha="right")
a2.text(1.2e-3, 57, "$E_{Na}$ ≈ +61 mV", fontsize=8, color=C["red"], va="top")
for rr, lab, off in ((0.04, "휴지 0.04", (-6, 14)), (4, "활동전위 정점 약 4", (6, -8))):
    v = ghk(5, rr)
    a2.plot([rr], [v], "o", color=C["ink"], ms=4.5, zorder=4)
    a2.annotate(f"{lab}\n{v:+.0f} mV".replace("-", "−"), xy=(rr, v), xytext=off, textcoords="offset points",
                fontsize=8, ha="right" if off[0] < 0 else "left", va="bottom" if off[1] > 0 else "top")
a2.set_xlabel("$P_{Na}/P_K$ (로그 눈금)")
a2.set_ylabel("막전위 (mV)")
a2.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100])
a2.set_xticklabels(["0.001", "0.01", "0.1", "1", "10", "100"])
a2.minorticks_off()
a2.set_ylim(-100, 70)
a2.set_yticks([-90, -60, -30, 0, 30, 60])
a2.set_yticklabels(["−90", "−60", "−30", "0", "30", "60"])
a2.set_title("(나) 투과도 비가 정하는 줄다리기", fontsize=10)
fig.tight_layout()
save(fig, __file__)
