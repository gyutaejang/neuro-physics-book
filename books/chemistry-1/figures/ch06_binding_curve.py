from figstyle import plt, np, save, C

Kd = 1.0  # nM
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0))

L = np.linspace(0, 10, 400)
a1.plot(L, L / (L + Kd) * 100, color=C["blue"], lw=1.6)
a1.plot([0, Kd, Kd], [50, 50, 0], color=C["gray"], lw=0.8, ls="--")
a1.text(Kd + 0.15, 4, "$K_d$", fontsize=10)
a1.annotate("농도를 2배, 4배 늘려도\n점유율은 조금씩만 오른다", xy=(6, 6 / 7 * 100), xytext=(3.2, 40),
            fontsize=8.5, arrowprops=dict(arrowstyle="->", color=C["gray"]))
a1.set_xlabel("리간드 농도 [L] ($K_d$의 배수)")
a1.set_ylabel("점유율 θ (%)")
a1.set_title("선형 눈금: 쌍곡선")
a1.set_ylim(0, 105)

Lg = np.logspace(-3, 3, 400)
a2.semilogx(Lg, Lg / (Lg + Kd) * 100, color=C["blue"], lw=1.6)
a2.axvspan(1 / 9, 9, color=C["light"], lw=0)
for x, y in ((1 / 9, 10), (1, 50), (9, 90)):
    a2.scatter([x], [y], color=C["red"], s=22, zorder=4)
a2.text(1 / 9 * 1.25, 10, "10 %", fontsize=8.5, va="center")
a2.text(1 * 1.3, 48, "50 % ($K_d$)", fontsize=8.5, va="top")
a2.text(9 * 1.3, 88, "90 %", fontsize=8.5, va="top")
a2.text(1, 104, "81배 (약 2자릿수)", ha="center", va="bottom", fontsize=8.5)
a2.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
a2.set_xticklabels(["1/1000", "1/100", "1/10", "1", "10", "100", "1000"])
a2.minorticks_off()
a2.set_xlabel("[L] / $K_d$ (로그 눈금)")
a2.set_title("로그 눈금: S자 곡선")
a2.set_ylim(0, 115)
a2.set_yticks([0, 25, 50, 75, 100])
fig.tight_layout()
save(fig, __file__)
