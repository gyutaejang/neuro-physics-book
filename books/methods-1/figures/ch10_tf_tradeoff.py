from figstyle import plt, np, save, C
from scipy.signal import fftconvolve

# 모를레 웨이블릿 시간-주파수 분석의 맞바꿈.
# 0.6–1.4 s: 10 Hz와 14 Hz가 함께 있다. 2.00 s와 2.12 s: 40 Hz 짧은 버스트 두 개.
fs = 500
t = np.arange(0, 3, 1 / fs)
rng = np.random.default_rng(2)
env1 = np.where((t > 0.6) & (t < 1.4), np.sin(np.pi * (t - 0.6) / 0.8) ** 2, 0)
x = env1 * (np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 14 * t))
for tc in (2.00, 2.12):
    x += 1.5 * np.exp(-0.5 * ((t - tc) / 0.018) ** 2) * np.sin(2 * np.pi * 40 * (t - tc))
x += 0.15 * rng.standard_normal(len(t))


def morlet_tfr(x, fs, freqs, n_cycles):
    """복소 모를레 웨이블릿과 합성곱해 진폭을 구한다. 진폭 1인 사인파가 1로 나오게 정규화한다."""
    out = np.empty((len(freqs), len(x)))
    for i, f in enumerate(freqs):
        sd = n_cycles / (2 * np.pi * f)                 # 시간 표준편차 (s)
        tw = np.arange(-4 * sd, 4 * sd, 1 / fs)
        g = np.exp(-0.5 * (tw / sd) ** 2)
        w = g * np.exp(2j * np.pi * f * tw) / g.sum() * 2
        out[i] = np.abs(fftconvolve(x, w, mode="same"))
    return out


freqs = np.arange(4, 61, 0.5)
fig = plt.figure(figsize=(7.3, 4.4))
gs = fig.add_gridspec(2, 2, height_ratios=[0.55, 1.3], hspace=0.55, wspace=0.12)
ax = fig.add_subplot(gs[0, :])
ax.plot(t, x, color=C["blue"], lw=0.6)
ax.set_xlim(0, 3)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.text(1.0, 2.25, "10 Hz + 14 Hz (0.8 s)", ha="center", fontsize=8)
ax.text(2.06, 2.25, "40 Hz 버스트 두 개 (120 ms 간격)", ha="center", fontsize=8)
ax.set_ylim(-2.3, 2.9)
ax.set_xlabel("시간 (s)", fontsize=8.5, labelpad=1)
ax.tick_params(labelsize=8)
ax.set_title("(가) 합성 신호", fontsize=10)

for k, nc in enumerate([3, 12]):
    ax = fig.add_subplot(gs[1, k])
    A = morlet_tfr(x, fs, freqs, nc)
    ax.pcolormesh(t, freqs, A / A.max(), cmap="viridis", shading="auto", vmin=0, vmax=1, rasterized=True)
    ax.set_xlim(0.3, 2.7)
    ax.set_xlabel("시간 (s)")
    if k == 0:
        ax.set_ylabel("주파수 (Hz)")
    else:
        ax.set_yticklabels([])
    for f0 in (10, 40):
        st = nc / (2 * np.pi * f0) * 1000
        sf = f0 / nc
        print(f"n={nc} f={f0}: sigma_t {st:.0f} ms, sigma_f {sf:.2f} Hz, FWHM_t {2.355*st:.0f} ms, FWHM_f {2.355*sf:.2f} Hz")
    st10 = nc / (2 * np.pi * 10) * 1000
    st40 = nc / (2 * np.pi * 40) * 1000
    ax.text(0.03, 0.97, f"{nc}주기 웨이블릿\n10 Hz: σt {st10:.0f} ms, σf {10 / nc:.1f} Hz\n40 Hz: σt {st40:.0f} ms, σf {40 / nc:.1f} Hz",
            transform=ax.transAxes, fontsize=7.5, va="top", color="white")
    ax.set_title(["(나) 짧은 웨이블릿: 시간이 날카롭다", "(다) 긴 웨이블릿: 주파수가 날카롭다"][k], fontsize=10)
save(fig, __file__)
