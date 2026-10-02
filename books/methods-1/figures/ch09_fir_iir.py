from scipy import signal

from figstyle import plt, np, save, C

# 표본화 500 Hz, 30 Hz 저역 통과 필터 두 가지.
fs = 500.0
# FIR: 해밍 창 sinc, 전이 대역 7.5 Hz → 길이 N ≈ 3.3 fs / Δf = 220 → 홀수 221 탭
N = 221
b_fir = signal.firwin(N, 30 + 7.5 / 2, window="hamming", fs=fs)
# IIR: 4차 버터워스
b_iir, a_iir = signal.butter(4, 30, btype="low", fs=fs)

f, H_fir = signal.freqz(b_fir, 1, worN=8192, fs=fs)
_, H_iir = signal.freqz(b_iir, a_iir, worN=8192, fs=fs)
db = lambda H: 20 * np.log10(np.maximum(np.abs(H), 1e-6))

fig = plt.figure(figsize=(7.4, 2.9))
gs = fig.add_gridspec(1, 3, wspace=0.45)

# (가) 크기 응답
a1 = fig.add_subplot(gs[0, 0])
a1.plot(f, db(H_fir), color=C["blue"], lw=1.6, label="FIR")
a1.plot(f, db(H_iir), color=C["red"], lw=1.4, ls="--", label="IIR")
a1.axvline(30, color=C["gray"], lw=0.6, ls=":")
a1.set_xlim(0, 80)
a1.set_ylim(-90, 8)
a1.set_xlabel("주파수 (Hz)")
a1.set_ylabel("이득 (dB)")
a1.set_title("(가) 크기 응답", fontsize=9.5)
a1.legend(fontsize=7.5, loc="lower left", handlelength=1.5)

# (나) 충격 응답
a2 = fig.add_subplot(gs[0, 1])
t_fir = np.arange(N) / fs * 1000
imp = np.zeros(400)
imp[0] = 1
h_iir = signal.lfilter(b_iir, a_iir, imp)
t_iir = np.arange(400) / fs * 1000
a2.axhline(0, color=C["gray"], lw=0.5)
a2.plot(t_fir, b_fir / b_fir.max(), color=C["blue"], lw=1.4)
a2.plot(t_iir, h_iir / h_iir.max(), color=C["red"], lw=1.3, ls="--")
a2.axvline((N - 1) / 2 / fs * 1000, color=C["blue"], lw=0.6, ls=":")
a2.text((N - 1) / 2 / fs * 1000 + 8, 0.85, "가운데\n220 ms", fontsize=7.5, color=C["blue"])
a2.text(45, -0.56, "IIR: 시작 직후에 몰린\n비대칭 꼬리", fontsize=7.5, color=C["red"])
a2.set_xlim(0, 460)
a2.set_ylim(-0.62, 1.15)
a2.set_xlabel("시간 (ms)")
a2.set_ylabel("충격 응답")
a2.set_title("(나) 충격 응답", fontsize=9.5)

# (다) 군지연
a3 = fig.add_subplot(gs[0, 2])
fg = np.linspace(0.5, 45, 300)
_, gd_fir = signal.group_delay((b_fir, 1), w=fg, fs=fs)
_, gd_iir = signal.group_delay((b_iir, a_iir), w=fg, fs=fs)
a3.plot(fg, gd_fir / fs * 1000, color=C["blue"], lw=1.6)
a3.plot(fg, gd_iir / fs * 1000, color=C["red"], lw=1.4, ls="--")
a3.text(3, 205, "FIR: 모든 주파수 220 ms", fontsize=7.5, color=C["blue"])
a3.text(3, 45, "IIR: 주파수마다 다름", fontsize=7.5, color=C["red"])
a3.set_xlim(0, 45)
a3.set_ylim(0, 250)
a3.set_xlabel("주파수 (Hz)")
a3.set_ylabel("지연 (ms)")
a3.set_title("(다) 군지연 (인과 적용)", fontsize=9.5)

save(fig, __file__)
