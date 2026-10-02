from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9))

m = np.logspace(0, 5, 400)
for alpha, col, lab in [(0.05, C["red"], "α = 0.05"), (0.001, C["blue"], "α = 0.001"),
                        (0.05 / 1e5, C["gray"], "α = 0.05/10⁵ (본페로니)")]:
    a1.plot(m, 1 - (1 - alpha) ** m, color=col, lw=1.8, label=lab)
for mm in (14, 100):
    f = 1 - 0.95 ** mm
    a1.scatter([mm], [f], color=C["red"], s=18, zorder=3)
    a1.text(mm * 1.5, f - 0.06, f"{mm}번: {f * 100:.1f} %", fontsize=8, color=C["red"], va="top")
a1.set_xscale("log")
a1.set_xlim(1, 1e5)
a1.set_ylim(0, 1.05)
a1.set_xlabel("독립 검정 수 $m$")
a1.set_ylabel("FWER (거짓 양성 ≥ 1개)")
a1.set_title("(가) 가족 오류율 $1-(1-α)^m$", fontsize=9.5)
a1.legend(fontsize=7.5, loc="lower right", bbox_to_anchor=(1.0, 0.08))

for alpha, col in [(0.05, C["red"]), (0.01, C["purple"]), (0.001, C["blue"])]:
    a2.plot(m, alpha * m, color=col, lw=1.8)
    a2.text(1.3e5, alpha * 1e5, f"p < {alpha}: {alpha * 1e5:,.0f}개", fontsize=8, color=col, va="center")
a2.axhline(1, color=C["gray"], lw=0.6, ls=":")
a2.set_xscale("log")
a2.set_yscale("log")
a2.set_xlim(1, 1e5)
a2.set_ylim(1e-3, 2e4)
a2.set_xlabel("검정 수 $m$ (복셀 수)")
a2.set_ylabel("거짓 양성 기댓값 $mα$")
a2.set_title("(나) 거짓 양성의 기댓값", fontsize=9.5)
fig.tight_layout(w_pad=1.5)
save(fig, __file__)
