from figstyle import plt, np, save, C
from scipy import signal

# 비정현 파형(뮤 리듬처럼 아치 모양인 10 Hz)이 만드는 가짜 고조파.
fs = 500
dur = 60
t = np.arange(0, dur, 1 / fs)
rng = np.random.default_rng(8)
f0 = 10.0
# 순간 위상에 약간의 흔들림을 주어 실제 리듬처럼 만든다.
phase = 2 * np.pi * np.cumsum(f0 + 0.6 * np.convolve(rng.standard_normal(len(t)), np.ones(50) / 50, "same")) / fs
sine = np.cos(phase)
# 아치 모양: 기본파 + 같은 위상 관계의 2, 3배 고조파. 봉우리는 뾰족하고 골은 둥글다(뮤 리듬은 이것을 뒤집은 모양).
arch = np.cos(phase) + 0.32 * np.cos(2 * phase) + 0.1 * np.cos(3 * phase)
arch = arch / arch.std() * sine.std()
noise = 0.25 * rng.standard_normal(len(t))

fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw=dict(wspace=0.42, width_ratios=[1.15, 1, 1.05]))
ax = axs[0]
seg = (t >= 10) & (t < 10.3)
ax.plot((t[seg] - 10) * 1000, sine[seg] + 3.7, color=C["gray"], lw=1.2)
ax.plot((t[seg] - 10) * 1000, arch[seg], color=C["blue"], lw=1.2)
ax.text(5, 4.85, "사인파 10 Hz", fontsize=8, color=C["gray"])
ax.text(5, 2.0, "아치 모양 10 Hz", fontsize=8, color=C["blue"])
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_ylim(-1.2, 5.3)
ax.set_xlabel("시간 (ms)")
ax.set_title("(가) 같은 주기, 다른 모양", fontsize=10)

ax = axs[1]
for x, col, lab in [(sine + noise, C["gray"], "사인파"), (arch + noise, C["blue"], "아치 모양")]:
    f, P = signal.welch(x, fs=fs, nperseg=2 * fs, noverlap=fs)
    sel = (f >= 2) & (f <= 45)
    ax.semilogy(f[sel], P[sel], color=col, lw=1.1, label=lab)
for h in (20, 30):
    ax.annotate(f"{h} Hz", xy=(h, 2.0e-2 if h == 20 else 2.5e-3), xytext=(h + 3, 1.0e-1 if h == 20 else 1.5e-2), fontsize=7.5,
                color=C["red"], arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
ax.set_xlabel("주파수 (Hz)")
ax.set_ylabel("파워 (로그)")
ax.legend(fontsize=7, loc="upper right")
ax.set_title("(나) 스펙트럼", fontsize=10)

ax = axs[2]
b, a = signal.butter(4, [17, 23], btype="band", fs=fs)
beta = signal.filtfilt(b, a, arch + noise)
seg2 = (t >= 10) & (t < 10.3)
ax.plot((t[seg2] - 10) * 1000, arch[seg2] / 2 + 1.2, color=C["blue"], lw=1.0)
ax.plot((t[seg2] - 10) * 1000, beta[seg2], color=C["red"], lw=1.1)
ax.text(5, 2.05, "원 신호 (세로 0.5배)", fontsize=7.5, color=C["blue"])
ax.text(5, -0.95, "17–23 Hz 대역 통과", fontsize=7.5, color=C["red"])
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_ylim(-1.1, 2.4)
ax.set_xlabel("시간 (ms)")
ax.set_title("(다) 생기는 '베타'", fontsize=10)
# 고조파의 크기 확인
f, P = signal.welch(arch, fs=fs, nperseg=2 * fs, noverlap=fs)
for h in (10, 20, 30):
    print(h, P[np.argmin(abs(f - h))])
print("beta amplitude rms", beta.std(), "sine filtered rms", signal.filtfilt(b, a, sine + noise).std())
save(fig, __file__)
