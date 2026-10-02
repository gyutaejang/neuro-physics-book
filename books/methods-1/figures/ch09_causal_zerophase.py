from scipy import signal

from figstyle import plt, np, save, C

# 합성 ERP: 60 ms에 갑자기 시작하는 P1, 165 ms의 N1, 350 ms의 P3 (μV).
fs = 1000.0
t = np.arange(-1.0, 1.5, 1 / fs)


def gau(mu, sd, a):
    return a * np.exp(-0.5 * ((t - mu) / sd) ** 2)


def onsetbump(t0, tau, a):
    s = np.clip(t - t0, 0, None)
    y = (s / tau) ** 2 * np.exp(-s / tau)
    return a * y / y.max()


erp = onsetbump(0.060, 0.018, 5) + gau(0.165, 0.018, -7) + gau(0.350, 0.080, 6)

# 10 Hz 저역 통과: 4차 버터워스(인과 / 앞뒤 두 번), 가파른 FIR(지연 보정, 영위상)
bi, ai = signal.butter(4, 10, fs=fs)
causal = signal.lfilter(bi, ai, erp)
zphase = signal.filtfilt(bi, ai, erp)
N = int(3.3 * fs / 2.5) | 1
b = signal.firwin(N, 11.25, window="hamming", fs=fs)
zfir = np.convolve(erp, b, mode="same")


def onset(x, thr=0.5):
    return t[np.where(np.abs(x) > thr)[0][0]] * 1000


ms = t * 1000
fig = plt.figure(figsize=(7.3, 3.0))
gs = fig.add_gridspec(1, 2, wspace=0.25)

a1 = fig.add_subplot(gs[0, 0])
a1.axhline(0, color=C["gray"], lw=0.5)
a1.axvline(0, color=C["gray"], lw=0.5, ls=":")
a1.plot(ms, erp, color=C["gray"], lw=2.2, alpha=0.6, label="원래 ERP")
a1.plot(ms, causal, color=C["red"], lw=1.5, label="인과 IIR (한 방향)")
a1.text(150, 6.9, "정점이 약 40–50 ms 늦어진다", fontsize=7.8, color=C["red"])
a1.set_xlim(-100, 500)
a1.set_ylim(-8.5, 8)
a1.set_xlabel("자극 뒤 시간 (ms)")
a1.set_ylabel("전위 (μV)")
a1.set_title("(가) 인과 필터: 늦어지고 비대칭으로 번진다", fontsize=9.3)
a1.legend(fontsize=7.5, loc="lower left")

a2 = fig.add_subplot(gs[0, 1])
a2.axhline(0, color=C["gray"], lw=0.5)
a2.axvline(0, color=C["gray"], lw=0.5, ls=":")
a2.plot(ms, erp, color=C["gray"], lw=2.2, alpha=0.6, label="원래 ERP")
a2.plot(ms, zphase, color=C["blue"], lw=1.5, label="영위상 IIR (앞뒤 두 번)")
a2.plot(ms, zfir, color=C["purple"], lw=1.2, ls="--", label="영위상 FIR (가파름)")
for x, col in [(onset(erp), C["gray"]), (onset(zphase), C["blue"]), (onset(zfir), C["purple"])]:
    a2.plot([x, x], [-0.9, 0.9], color=col, lw=1.0)
a2.text(-95, -3.2, "시작점 (0.5 μV 문턱)", fontsize=7.6, color=C["ink"])
a2.text(-95, -4.6, f"원래 {onset(erp):.0f} ms", fontsize=7.6, color=C["gray"])
a2.text(-95, -5.9, f"영위상 IIR {onset(zphase):.0f} ms", fontsize=7.6, color=C["blue"])
a2.text(-95, -7.2, f"영위상 FIR {onset(zfir):.0f} ms", fontsize=7.6, color=C["purple"])
a2.set_xlim(-100, 500)
a2.set_ylim(-8.5, 8)
a2.set_xlabel("자극 뒤 시간 (ms)")
a2.set_title("(나) 영위상 필터: 제자리이지만 앞으로도 번진다", fontsize=9.3)
a2.legend(fontsize=7.5, loc="lower right")

save(fig, __file__)
