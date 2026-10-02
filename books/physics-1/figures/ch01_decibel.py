from figstyle import plt, np, save, C

db = np.linspace(-40, 40, 400)
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.semilogy(db, 10 ** (db / 10), color=C["blue"], label="파워 비 = 10^(dB/10)")
ax.semilogy(db, 10 ** (db / 20), color=C["red"], label="진폭 비 = 10^(dB/20)")
for d in (-20, 0, 20):
    ax.axvline(d, color=C["gray"], lw=0.6, ls=":")
ax.set_xlabel("데시벨 (dB)")
ax.set_ylabel("비율 (로그 눈금)")
ax.text(20.5, 100, "+20 dB\n파워 100배\n진폭 10배", fontsize=8.5, va="center")
ax.text(-19.5, 0.02, "−20 dB\n파워 1/100\n진폭 1/10", fontsize=8.5, va="center")
ax.text(0.5, 1.6, "0 dB = 같다", fontsize=8.5)
ax.legend(loc="upper left", fontsize=8.5)
save(fig, __file__)
