from figstyle import plt, np, save, C

rng = np.random.default_rng(7)
fs = 20000
T = 1.0
t = np.arange(0, T, 1 / fs)
n = t.size
f = np.fft.rfftfreq(n, 1 / fs)


def shaped_noise(lo, hi, slope):
    spec = np.zeros_like(f)
    m = (f >= lo) & (f <= hi)
    spec[m] = 1 / f[m] ** slope
    x = np.fft.irfft(spec * np.exp(2j * np.pi * rng.random(f.size)), n=n)
    return x / x.std()


# 느린 성분: 6 Hz 리듬 + 1/f 배경 (단위 μV)
slow = 250 * np.sin(2 * np.pi * 6 * t) + 80 * shaped_noise(1, 200, 1.0)
# 발화: 느린 성분이 음(흡입원)일 때 더 자주 발화
rate = 40 * np.exp(-slow / 150)          # Hz, 근처 뉴런 몇 개를 합친 비율
spikes = rng.random(n) < rate / fs
w_t = np.arange(-0.0006, 0.0012, 1 / fs)
wave = -np.exp(-0.5 * (w_t / 0.00015) ** 2) + 0.35 * np.exp(-0.5 * ((w_t - 0.0004) / 0.0003) ** 2)
amp = rng.uniform(60, 140, spikes.sum())
spk = np.zeros(n)
for i, a in zip(np.where(spikes)[0], amp):
    j0 = i + int(w_t[0] * fs)
    seg = slice(max(j0, 0), min(j0 + wave.size, n))
    spk[seg] += a * wave[: seg.stop - seg.start]
noise = 12 * rng.standard_normal(n)
raw = slow + spk + noise


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    g = np.ones_like(f)
    if lo:
        g *= 1 / (1 + (lo / np.maximum(f, 1e-9)) ** 8)
    if hi:
        g *= 1 / (1 + (f / hi) ** 8)
    return np.fft.irfft(X * g, n=n)


lfp = bandpass(raw, None, 300)
mua = bandpass(raw, 300, 5000)

fig, axes = plt.subplots(3, 1, figsize=(7.0, 3.9), sharex=True)
rows = [(raw, "원신호 (넓은 대역)", C["ink"], 420),
        (lfp, "LFP (300 Hz 아래)", C["blue"], 420),
        (mua, "MUA (300 Hz 위)", C["red"], 220)]
for ax, (y, lab, col, lim) in zip(axes, rows):
    ax.plot(t * 1000, y, color=col, lw=0.5)
    ax.set_ylim(-lim, lim)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(1005, 0, lab, fontsize=8.5, va="center", ha="left", color=col)
    ax.plot([-15, -15], [-100, 100], color=C["ink"], lw=1.2, clip_on=False)
for ax in axes:
    ax.text(-25, 0, "200 μV", fontsize=7.5, va="center", ha="right")
axes[2].text(500, -205, "발화는 LFP의 골(음의 전위) 근처에 몰린다", fontsize=7.5, ha="center", va="bottom", color=C["gray"])
axes[2].set_xlabel("시간 (ms)")
axes[2].set_xlim(0, 1000)
for ax in axes[:2]:
    ax.tick_params(axis="x", length=0)
    ax.spines["bottom"].set_visible(False)
axes[0].set_title("같은 전극, 두 가지 신호: 주파수로 나눈다", fontsize=10)
fig.tight_layout()
fig.subplots_adjust(left=0.1, right=0.8, hspace=0.12)
save(fig, __file__)
