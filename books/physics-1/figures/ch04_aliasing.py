from figstyle import plt, np, save, C

f_card, TR = 1.1, 2.0
t = np.linspace(0, 30, 6000)
ts = np.arange(0, 30.01, TR)
fig, ax = plt.subplots(figsize=(7.0, 2.9))
ax.plot(t, np.cos(2 * np.pi * f_card * t), color=C["gray"], lw=0.6, label="실제 심장 박동 성분 1.1 Hz")
ax.plot(t, np.cos(2 * np.pi * 0.1 * t), color=C["red"], lw=1.6, ls="--", label="표본이 그려 내는 가짜 파 0.1 Hz")
ax.plot(ts, np.cos(2 * np.pi * f_card * ts), "o", color=C["red"], ms=5, zorder=3, label="TR = 2 s 표본")
ax.set_xlabel("시간 (s)")
ax.set_yticks([])
ax.set_ylim(-1.3, 2.1)
ax.set_xlim(0, 30)
ax.legend(fontsize=8.5, ncol=3, loc="upper center", handlelength=1.5, columnspacing=1.0)
fig.tight_layout()
save(fig, __file__)
