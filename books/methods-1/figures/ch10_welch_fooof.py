from figstyle import plt, np, save, C
from scipy import signal
from scipy.optimize import curve_fit

# 합성 휴지기 EEG 60 s: 비주기 1/f^χ 배경 + 10 Hz 알파 봉우리. 웰치 스펙트럼에 FOOOF 비슷한 모형을 적합한다.
fs, dur = 250, 60
n = fs * dur
rng = np.random.default_rng(5)
fr = np.fft.rfftfreq(n, 1 / fs)


def synth(chi, pivot=30.0, peak=0.35):
    """파워 스펙트럼 모양을 정해 무작위 위상으로 시계열을 만든다.
    pivot Hz에서 비주기 파워를 1로 맞추고, 알파 봉우리는 로그 파워에서 비주기 위로 peak만큼 솟게 한다."""
    P = np.zeros_like(fr)
    P[1:] = (fr[1:] / pivot) ** (-chi) * 10 ** (peak * np.exp(-0.5 * ((fr[1:] - 10.0) / 1.0) ** 2))
    X = np.sqrt(P) * np.exp(2j * np.pi * rng.random(len(fr)))
    X[0] = 0
    return np.fft.irfft(X, n)


def model(f, b, chi, *g):
    y = b - chi * np.log10(f)
    for k in range(0, len(g), 3):
        a, c, w = g[k:k + 3]
        y = y + a * np.exp(-0.5 * ((f - c) / w) ** 2)
    return y


def fit_spectrum(f, P, max_peaks=3):
    """FOOOF식 3단계: (1) 비주기 적합 → (2) 평탄화 스펙트럼에서 가우스 봉우리 찾기 → (3) 전체 동시 적합."""
    L = np.log10(P)
    lf = np.log10(f)
    chi0, b0 = np.polyfit(lf, L, 1)
    res = L - (b0 + chi0 * lf)
    keep = res < np.percentile(res, 40)                       # 봉우리를 피해 낮은 점들로 다시 적합
    chi0, b0 = np.polyfit(lf[keep], L[keep], 1)
    flat = L - (b0 + chi0 * lf)
    guess, resid = [], flat.copy()
    thr = max(2.0 * np.std(flat[keep]), 0.1)              # 잡음 출렁임보다 높고, 최소 0.1
    for _ in range(max_peaks):
        i = resid.argmax()
        if resid[i] < thr:
            break
        guess += [resid[i], f[i], 1.0]
        resid = resid - resid[i] * np.exp(-0.5 * ((f - f[i]) / 1.0) ** 2)
    p0 = [b0, -chi0] + guess
    lo = [-np.inf, 0] + [0, f[0], 0.5] * (len(guess) // 3)
    hi = [np.inf, 5] + [np.inf, f[-1], 6] * (len(guess) // 3)
    popt, _ = curve_fit(model, f, L, p0=p0, bounds=(lo, hi), maxfev=20000)
    return popt, flat


x1 = synth(1.5)
f, P1 = signal.welch(x1, fs=fs, nperseg=2 * fs, noverlap=fs, window="hann")
sel = (f >= 2) & (f <= 40)
f, P1 = f[sel], P1[sel]
popt1, flat1 = fit_spectrum(f, P1)
print("fit 1: offset %.2f exponent %.2f" % (popt1[0], popt1[1]), "peaks", np.round(popt1[2:], 2))

fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw=dict(wspace=0.42))
ax = axs[0]
ax.loglog(f, P1, color=C["blue"], lw=1.2, label="웰치 스펙트럼")
ax.loglog(f, 10 ** model(f, *popt1), color=C["red"], lw=1.0, label="모형 전체")
ax.loglog(f, 10 ** model(f, *popt1[:2]), color=C["gray"], lw=1.0, ls="--", label=f"비주기: χ = {popt1[1]:.2f}")
ax.set_xticks([2, 5, 10, 20, 40])
ax.set_xticklabels(["2", "5", "10", "20", "40"])
ax.minorticks_off()
ax.set_xlabel("주파수 (Hz, 로그)")
ax.set_ylabel("파워 (임의 단위, 로그)")
ax.legend(fontsize=7, loc="lower left")
ax.set_title("(가) 로그-로그 스펙트럼", fontsize=10)

ax = axs[1]
flat_fit = model(f, *popt1) - model(f, *popt1[:2])
ax.plot(f, np.log10(P1) - model(f, *popt1[:2]), color=C["blue"], lw=1.1, label="스펙트럼 − 비주기")
ax.plot(f, flat_fit, color=C["red"], lw=1.0, label="가우스 봉우리")
ax.axhline(0, color=C["gray"], lw=0.6)
a, cf, w = popt1[2:5]
ax.text(20, a * 0.62, f"중심 {cf:.1f} Hz\n높이 {a:.2f}\n폭 σ {w:.1f} Hz", fontsize=7.5, va="center", ha="left")
ax.set_xlim(2, 40)
ax.set_xlabel("주파수 (Hz)")
ax.set_ylabel("log₁₀ 파워 차")
ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.0, 1.02))
ax.set_ylim(-0.12, a * 1.5)
ax.set_xticks([2, 10, 20, 30, 40])
ax.set_title("(나) 평탄화한 스펙트럼", fontsize=10)

ax = axs[2]
x2 = synth(2.0)
_, P2 = signal.welch(x2, fs=fs, nperseg=2 * fs, noverlap=fs, window="hann")
P2 = P2[sel]
popt2, _ = fit_spectrum(f, P2)
print("fit 2: offset %.2f exponent %.2f" % (popt2[0], popt2[1]), "peaks", np.round(popt2[2:], 2))
ax.loglog(f, P1, color=C["blue"], lw=1.1, label="χ = 1.5")
ax.loglog(f, P2, color=C["purple"], lw=1.1, label="χ = 2.0")
ax.axvspan(8, 13, color=C["light"], zorder=0)
band = (f >= 8) & (f <= 13)
bp1, bp2 = np.trapezoid(P1[band], f[band]), np.trapezoid(P2[band], f[band])
print("alpha band power ratio", bp2 / bp1, "peak heights", popt1[2], popt2[2])
ax.text(0.62, 0.42, f"8–13 Hz 파워\n{bp2 / bp1:.1f}배 차이\n\n봉우리 높이\n{popt1[2]:.2f} 대 {popt2[2]:.2f}",
        transform=ax.transAxes, fontsize=7, ha="left", va="bottom")
ax.set_xticks([2, 5, 10, 20, 40])
ax.set_xticklabels(["2", "5", "10", "20", "40"])
ax.minorticks_off()
ax.set_xlabel("주파수 (Hz, 로그)")
ax.legend(fontsize=7, loc="upper right")
ax.set_title("(다) 기울기만 다를 때", fontsize=10)
save(fig, __file__)
