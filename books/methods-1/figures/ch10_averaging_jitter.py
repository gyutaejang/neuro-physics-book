from figstyle import plt, np, save, C

# 합성 ERP: P1(+3 μV, 100 ms), N1(−4 μV, 170 ms), P3(+8 μV, 350 ms)의 가우스 합.
fs = 500
t = np.arange(-0.2, 0.8, 1 / fs)
comps = [(3.0, 0.100, 0.015), (-4.0, 0.170, 0.020), (8.0, 0.350, 0.060)]


def erp(tt, shift=0.0):
    return sum(a * np.exp(-0.5 * ((tt - mu - shift) / s) ** 2) for a, mu, s in comps)


rng = np.random.default_rng(3)


def bg_noise(n, sd=20.0):
    """1/f 모양의 배경 EEG (표준편차 sd μV)."""
    nt = len(t)
    f = np.fft.rfftfreq(nt, 1 / fs)
    amp = np.zeros_like(f)
    amp[1:] = 1 / np.sqrt(f[1:])
    X = (rng.standard_normal((n, len(f))) + 1j * rng.standard_normal((n, len(f)))) * amp
    x = np.fft.irfft(X, nt, axis=1)
    return x / x.std(axis=1, keepdims=True) * sd


true = erp(t)
trials = true + bg_noise(400)

fig = plt.figure(figsize=(7.3, 3.5))
gs = fig.add_gridspec(3, 2, wspace=0.3, hspace=0.25)
for k, n in enumerate([1, 16, 400]):
    ax = fig.add_subplot(gs[k, 0])
    avg = trials[:n].mean(0)
    ax.plot(t * 1000, avg, color=C["gray"] if n == 1 else C["blue"], lw=0.7 if n == 1 else 0.9)
    ax.plot(t * 1000, true, color=C["red"], lw=1.0, ls="--")
    ax.axvline(0, color=C["gray"], lw=0.6)
    lim = [60, 18, 12][k]
    ax.set_ylim(-lim, lim)
    ax.set_xlim(-200, 800)
    ax.set_yticks([-lim // 2 * 1, 0, lim // 2 * 1] if k else [-40, 0, 40])
    ax.tick_params(labelsize=7.5)
    ax.text(0.01, 0.97, f"{['시행 1개', '16개 평균', '400개 평균'][k]} (잔여 잡음 약 {20 / np.sqrt(n):.0f} μV)",
            transform=ax.transAxes, fontsize=7.8, va="top", ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=0.5, alpha=0.8))
    if k < 2:
        ax.set_xticklabels([])
    if k == 0:
        ax.set_title("(가) 평균할수록 ERP가 드러난다", fontsize=10)
    if k == 1:
        ax.set_ylabel("전위 (μV)")
    if k == 2:
        ax.set_xlabel("자극 뒤 시간 (ms)")
axs = [None, fig.add_subplot(gs[:, 1])]
ax = axs[1]
for sj, col, lab in [(0, C["red"], "흔들림 없음"), (0.030, C["blue"], "흔들림 σ = 30 ms"), (0.060, C["purple"], "흔들림 σ = 60 ms")]:
    shifts = rng.standard_normal(4000) * sj
    avg = np.mean([erp(t, s) for s in shifts], axis=0)
    ax.plot(t * 1000, avg, color=col, lw=1.4 if sj == 0 else 1.2, ls="--" if sj == 0 else "-", label=lab)
ax.axhline(0, color=C["gray"], lw=0.6)
ax.axvline(0, color=C["gray"], lw=0.6)
ax.annotate("N1: 날카로운 성분이\n먼저 무너진다", xy=(178, -1.8), xytext=(300, -4.4), fontsize=7.8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6), va="center")
ax.annotate("P3: 폭이 넓어\n덜 줄어든다", xy=(420, 5.0), xytext=(540, 5.6), fontsize=7.8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6), va="center")
ax.set_xlim(-200, 800)
ax.set_ylim(-6, 9.5)
ax.set_xlabel("자극 뒤 시간 (ms)")
ax.set_ylabel("평균 전위 (μV)")
ax.legend(fontsize=7.5, loc="upper left")
ax.set_title("(나) 잠복기 흔들림은 평균을 뭉갠다", fontsize=10)
save(fig, __file__)
