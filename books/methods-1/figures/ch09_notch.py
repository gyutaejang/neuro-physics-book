from scipy import signal

from figstyle import plt, np, save, C

fs = 1000.0
t = np.arange(-1, 1, 1 / fs)
# 전원 잡음이 없는 깨끗한 신호: 바닥 폭 20 ms인 뾰족한 극파(−100 μV)와 뒤따르는 느린 파.
x = -100 * np.clip(1 - np.abs(t) / 0.010, 0, None) + 40 * np.exp(-0.5 * ((t - 0.12) / 0.05) ** 2)

fig = plt.figure(figsize=(7.4, 2.9))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.25], wspace=0.42)

a1 = fig.add_subplot(gs[0, 0])
f = np.linspace(40, 80, 2000)
for Q, col, ls in [(30, C["blue"], "-"), (5, C["red"], "--")]:
    b, a = signal.iirnotch(60, Q, fs=fs)
    _, H = signal.freqz(b, a, worN=f, fs=fs)
    a1.plot(f, 2 * 20 * np.log10(np.maximum(np.abs(H), 1e-5)), color=col, lw=1.5, ls=ls,
            label=f"Q = {Q}")
a1.set_xlim(40, 80)
a1.set_ylim(-60, 3)
a1.set_xlabel("주파수 (Hz)")
a1.set_ylabel("이득 (dB, 앞뒤 두 번)")
a1.set_title("(가) 60 Hz 노치", fontsize=9.5)
a1.legend(fontsize=7.3, loc="lower left", handlelength=1.4)

a2 = fig.add_subplot(gs[0, 1])
b5, a5 = signal.iirnotch(60, 5, fs=fs)
y5 = signal.filtfilt(b5, a5, x)
ms = t * 1000
a2.axhline(0, color=C["gray"], lw=0.5)
a2.plot(ms, x, color=C["gray"], lw=2.2, alpha=0.6, label="원래")
a2.plot(ms, y5, color=C["red"], lw=1.1, label="노치 뒤")
a2.set_xlim(-150, 250)
a2.set_ylim(-110, 50)
a2.set_xlabel("시간 (ms)")
a2.set_ylabel("전위 (μV)")
a2.set_title("(나) 극파에 노치를 걸면", fontsize=9.5)
a2.legend(fontsize=7.3, loc="lower right", handlelength=1.2)

a3 = fig.add_subplot(gs[0, 2])
a3.axhline(0, color=C["gray"], lw=0.5)
for Q, col, off in [(30, C["blue"], 0), (5, C["red"], -12)]:
    b, a = signal.iirnotch(60, Q, fs=fs)
    r = signal.filtfilt(b, a, x) - x
    a3.plot(ms, r + off, color=col, lw=0.8)
    a3.text(-390, off + 2.4, f"Q = {Q}", fontsize=7.8, color=col)
a3.set_xlim(-400, 400)
a3.set_ylim(-22, 6)
a3.set_yticks([0, -12])
a3.set_yticklabels(["0", "0"])
a3.plot([300, 300], [-20, -15], color=C["ink"], lw=1.2)
a3.text(312, -17.5, "5 μV", fontsize=7.5, va="center")
a3.set_xlabel("시간 (ms)")
a3.set_ylabel("필터가 더한 것 (μV)")
a3.set_title("(다) 극파 앞뒤의 60 Hz 울림", fontsize=9.5)

save(fig, __file__)
