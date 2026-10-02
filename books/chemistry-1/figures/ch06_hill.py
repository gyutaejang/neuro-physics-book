from figstyle import plt, np, save, C

x = np.logspace(-2, 2, 400)
fig, ax = plt.subplots(figsize=(7.0, 2.6))
for n, col, lab in ((0.5, C["gray"], "n = 0.5 (음의 협동성)"),
                    (1, C["blue"], "n = 1 (독립 결합)"),
                    (2.7, C["red"], "n = 2.7 (헤모글로빈)"),
                    (6, C["purple"], "n = 6")):
    ax.semilogx(x, x ** n / (x ** n + 1) * 100, color=col, lw=1.5, label=lab)
ax.axhline(50, color=C["gray"], lw=0.5, ls=":")
ax.axvline(1, color=C["gray"], lw=0.5, ls=":")
ax.set_xlabel("[L] / $K_{50}$ (로그 눈금)")
ax.set_ylabel("점유율 (%)")
ax.set_xticks([0.01, 0.1, 1, 10, 100])
ax.set_xticklabels(["1/100", "1/10", "1", "10", "100"])
ax.minorticks_off()
ax.legend(fontsize=8, loc="upper left")
ax.set_ylim(0, 102)
fig.tight_layout()
save(fig, __file__)
