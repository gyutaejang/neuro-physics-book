from figstyle import plt, np, save, C
from scipy.signal import fftconvolve

# 유발(위상 고정) 대 유도(위상 무작위) 활동. 시행 100개.
# 유발: 자극 뒤 약 150 ms의 5 Hz 짧은 파형(매 시행 같은 위상).
# 유도: 300–700 ms의 20 Hz 버스트(시행마다 위상이 무작위).
fs = 250
t = np.arange(-0.5, 1.2, 1 / fs)
ntr = 100
rng = np.random.default_rng(4)
nt = len(t)
fr = np.fft.rfftfreq(nt, 1 / fs)
amp = np.zeros_like(fr)
amp[1:] = 1 / fr[1:] ** 0.5


def bg(n):
    X = (rng.standard_normal((n, len(fr))) + 1j * rng.standard_normal((n, len(fr)))) * amp
    y = np.fft.irfft(X, nt, axis=1)
    return y / y.std()


evk = 1.2 * np.exp(-0.5 * ((t - 0.15) / 0.06) ** 2) * np.cos(2 * np.pi * 5 * (t - 0.15))
env = np.exp(-0.5 * ((t - 0.5) / 0.12) ** 2)
ph = rng.uniform(0, 2 * np.pi, ntr)[:, None]
ind = 1.0 * env * np.cos(2 * np.pi * 20 * t + ph)
trials = evk + ind + bg(ntr)

freqs = np.arange(3, 41, 0.5)


def morlet_coefs(x, n_cycles=5):
    out = np.empty((x.shape[0], len(freqs), nt), complex)
    for i, f in enumerate(freqs):
        sd = n_cycles / (2 * np.pi * f)
        tw = np.arange(-4 * sd, 4 * sd, 1 / fs)
        g = np.exp(-0.5 * (tw / sd) ** 2)
        w = g * np.exp(2j * np.pi * f * tw) / g.sum() * 2
        out[:, i] = fftconvolve(x, w[None, :], mode="same", axes=1)
    return out


W = morlet_coefs(trials)
total = (np.abs(W) ** 2).mean(0)                          # 시행마다 파워를 구해 평균
erp = trials.mean(0, keepdims=True)
evoked = np.abs(morlet_coefs(erp)[0]) ** 2                # 평균 파형(ERP)의 파워
itc = np.abs((W / np.abs(W)).mean(0))                     # 시행 간 위상 일치도
base = (t >= -0.4) & (t <= -0.1)


def db(P):
    return 10 * np.log10(P / P[:, base].mean(1, keepdims=True))


crop = (t >= -0.3) & (t <= 1.0)
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw=dict(wspace=0.12))
panels = [(db(total), "(가) 전체 파워 (dB)", "RdBu_r", (-6, 6)),
          (evoked / evoked[:, crop].max(),
           "(나) ERP의 파워 (최댓값 = 1)", "Reds", (0, 1)),
          (itc, "(다) ITC", "viridis", (0, 0.8))]
for k, (Z, title, cmap, (lo, hi)) in enumerate(panels):
    ax = axs[k]
    im = ax.pcolormesh(t[crop] * 1000, freqs, Z[:, crop], cmap=cmap, vmin=lo, vmax=hi, shading="auto", rasterized=True)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel("자극 뒤 시간 (ms)")
    ax.set_title(title, fontsize=10)
    ax.set_xticks([0, 500])
    if k == 0:
        ax.set_ylabel("주파수 (Hz)")
    else:
        ax.set_yticklabels([])
    cb = fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.25, fraction=0.06, aspect=22)
    cb.ax.tick_params(labelsize=7)
axs[0].text(520, 27, "유도\n20 Hz", fontsize=7.5, color="k", ha="center")
axs[0].text(160, 11, "유발", fontsize=7.5, color="k", ha="center")
i20 = np.argmin(abs(freqs - 20)); i5 = np.argmin(abs(freqs - 5))
it5 = np.argmin(abs(t - 0.15)); it20 = np.argmin(abs(t - 0.5))
print("ITC at 5 Hz/150 ms", itc[i5, it5], "ITC at 20 Hz/500 ms", itc[i20, it20])
print("baseline ITC mean", itc[:, base].mean(), "expected", np.sqrt(np.pi / (4 * ntr)))
print("total dB at 20Hz/500", db(total)[i20, it20])
save(fig, __file__)
