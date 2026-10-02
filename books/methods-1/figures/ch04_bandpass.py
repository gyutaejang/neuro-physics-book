from scipy.signal import butter, sosfiltfilt, welch

from figstyle import plt, np, save, C

# 연속 시간(20 Hz)에서 만든 신호를 TR 2 s로 표본화한다. 나이퀴스트 0.25 Hz.
TR, NV = 2.0, 300
fs_hi = 20.0
th = np.arange(0, NV * TR, 1 / fs_hi)
rng = np.random.default_rng(5)


def band_hi(fl, fh):
    f = np.fft.rfftfreq(th.size, 1 / fs_hi)
    X = rng.normal(size=f.size) + 1j * rng.normal(size=f.size)
    X[(f < fl) | (f > fh)] = 0
    x = np.fft.irfft(X, th.size)
    return x / x.std()


neural = band_hi(0.01, 0.1)
drift = 5.0 * (th / th[-1]) ** 1.5 + 0.8 * np.sin(2 * np.pi * th / 900)
card = 0.9 * np.sin(2 * np.pi * 1.15 * th)                  # 심박 1.15 Hz
resp = 0.7 * np.sin(2 * np.pi * 0.30 * th + 1.0)            # 호흡 0.30 Hz
idx = (np.arange(NV) * TR * fs_hi).astype(int)
y = (neural + drift + card + resp)[idx] + rng.normal(0, 0.5, NV)
t = np.arange(NV) * TR
fal_c = abs(1.15 - round(1.15 / 0.5) * 0.5)
fal_r = abs(0.30 - round(0.30 / 0.5) * 0.5)
print("aliased cardiac", fal_c, "resp", fal_r)

sos = butter(2, [0.01, 0.1], btype="band", fs=1 / TR, output="sos")
yf = sosfiltfilt(sos, y - y.mean())
f, P = welch(y - y.mean(), fs=1 / TR, nperseg=150, detrend=False)
_, Pf = welch(yf, fs=1 / TR, nperseg=150, detrend=False)
print("kept fraction of freq axis", (0.1 - 0.01) / 0.25)
print("corr with neural before", np.corrcoef(y, neural[idx])[0, 1].round(2),
      "after", np.corrcoef(yf, neural[idx])[0, 1].round(2))

fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.3))
a.axvspan(0.01, 0.1, color=C["light"], zorder=0)
a.semilogy(f, P, color=C["gray"], lw=1.2, label="필터 전")
a.semilogy(f, Pf, color=C["blue"], lw=1.4, label="필터 뒤")
a.annotate("심박 1.15 Hz\n→ 0.15 Hz로 접힘", xy=(0.15, P[np.argmin(abs(f - 0.15))] * 1.3), xytext=(0.143, 4e2),
           fontsize=7.5, color=C["red"], ha="right", va="top",
           arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.7))
a.annotate("호흡 0.30 Hz\n→ 0.20 Hz", xy=(0.2, P[np.argmin(abs(f - 0.2))] * 1.3), xytext=(0.207, 4e2),
           fontsize=7.5, color=C["red"], ha="left", va="top",
           arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.7))
a.annotate("표류", xy=(f[1], P[1]), xytext=(0.03, 3e2), fontsize=7.5, color=C["gray"], va="top",
           arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.7))
a.set_xlim(0, 0.25)
a.set_ylim(1e-3, 1e3)
a.set_xlabel("주파수 (Hz, 나이퀴스트 0.25 Hz까지)")
a.set_ylabel("파워 (상대)")
a.legend(fontsize=7.5, loc="lower right", bbox_to_anchor=(1.03, -0.02))
a.set_title("(가) 스펙트럼: 회색 띠가 통과 대역", fontsize=10, loc="left")

z = lambda s: (s - s.mean()) / s.std()
b.plot(t, z(y) + 5, color=C["gray"], lw=0.9)
b.plot(t, z(yf), color=C["blue"], lw=1.0)
b.plot(t, z(neural[idx]) - 5, color=C["green"], lw=1.0)
for yy, s_, c in ((5, "필터 전", C["gray"]), (0, "필터 뒤", C["blue"]), (-5, "참 신경 신호", C["green"])):
    b.text(605, yy, s_, fontsize=7.5, color=c, va="center")
b.set_yticks([])
b.spines["left"].set_visible(False)
b.set_xlim(0, 600)
b.set_xlabel("시간 (s)")
b.set_title("(나) 시계열 (각각 z 점수)", fontsize=10, loc="left")
save(fig, __file__)
