from figstyle import plt, np, save, C

rng = np.random.default_rng(11)
fs = 250
t = np.arange(-0.2, 0.8, 1 / fs)
n = t.size
f = np.fft.rfftfreq(n, 1 / fs)
true = (-5 * np.exp(-0.5 * ((t - 0.10) / 0.025) ** 2)
        + 4 * np.exp(-0.5 * ((t - 0.18) / 0.03) ** 2)
        + 10 * np.exp(-0.5 * ((t - 0.35) / 0.08) ** 2))


def eeg_noise(k):
    spec = np.zeros_like(f)
    m = (f >= 0.5) & (f <= 30)
    spec[m] = 1 / f[m] ** 0.8
    spec[(f > 8) & (f < 12)] *= 2.0  # 알파 봉우리
    X = spec * np.exp(2j * np.pi * rng.random((k, f.size)))
    x = np.fft.irfft(X, n=n, axis=1)
    return x / x.std(axis=1, keepdims=True) * 20  # 배경 EEG 실효값 20 μV


trials = true + eeg_noise(400)
fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7), sharey=True)
for ax, N in zip(axes, (1, 16, 400)):
    avg = trials[:N].mean(axis=0)
    resid = (avg - true)[t < 0].std()
    ax.axvline(0, color=C["gray"], lw=0.6, ls=":")
    ax.axhline(0, color=C["gray"], lw=0.5)
    ax.plot(t * 1000, true, color=C["red"], lw=1.2, ls="--")
    ax.plot(t * 1000, avg, color=C["blue"], lw=1.0)
    ax.set_title(f"{N}회 평균 (잡음 약 {20 / np.sqrt(N):.0f} μV)" if N > 1 else "한 번의 시행 (잡음 약 20 μV)",
                 fontsize=9)
    ax.set_xlabel("자극 후 시간 (ms)")
    ax.set_xticks([0, 300, 600])
    ax.set_ylim(-65, 65)
axes[0].set_ylabel("전위 (μV)")
axes[2].annotate("P300", xy=(350, 10.5), xytext=(500, 38), fontsize=8, color=C["red"],
                 arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
axes[2].annotate("N100", xy=(100, -5.5), xytext=(150, -38), fontsize=8, color=C["red"],
                 arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
axes[1].text(-180, 58, "점선: 실제 반응", fontsize=7.5, color=C["red"], va="top")
fig.tight_layout()
save(fig, __file__)
