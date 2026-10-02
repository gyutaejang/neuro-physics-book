import math

from figstyle import plt, np, save, C

# 합성곱 정리: 시간 영역의 합성곱 = 주파수 영역의 곱. 20 s 켜짐/20 s 꺼짐 블록과 표준 HRF.
dt = 0.1
t = np.arange(0, 400, dt)                  # 블록 10주기
stim = ((t % 40) < 20).astype(float)
th = np.arange(0, 32, dt)
g = lambda u, a: u ** (a - 1) * np.exp(-u) / math.gamma(a)
h = g(th, 6) - g(th, 16) / 6
h = h / h.max()
# 주기 신호로 보고 원형 합성곱을 한다 (시작 부분의 과도 반응이 없게)
bold = np.real(np.fft.ifft(np.fft.fft(stim) * np.fft.fft(h, len(t)))) * dt
bold = bold / bold.max()

f = np.fft.rfftfreq(len(t), dt)            # 간격 1/400 Hz
S = np.abs(np.fft.rfft(stim - stim.mean()))
Y = np.abs(np.fft.rfft(bold - bold.mean()))
nf = 2 ** 16
fh = np.fft.rfftfreq(nf, dt)
H = np.abs(np.fft.rfft(h, nf))

fig, axes = plt.subplots(2, 3, figsize=(7.4, 4.3), gridspec_kw={"hspace": 0.8, "wspace": 0.35})
axes[0, 0].plot(t, stim, color=C["green"])
axes[0, 0].set_ylim(-0.1, 1.3)
axes[0, 0].set_title("(가) 자극: 20 s 켜짐/꺼짐", fontsize=9.5)
axes[0, 1].plot(th, h, color=C["blue"])
axes[0, 1].axhline(0, color=C["gray"], lw=0.5)
axes[0, 1].set_title("(나) ∗ HRF", fontsize=9.5)
axes[0, 1].set_xlim(0, 32)
axes[0, 2].plot(t, bold, color=C["red"])
axes[0, 2].axhline(0, color=C["gray"], lw=0.5)
axes[0, 2].set_title("(다) = 예측 BOLD", fontsize=9.5)
for a in (axes[0, 0], axes[0, 2]):
    a.set_xlim(0, 120)
for a in axes[0]:
    a.set_xlabel("시간 (s)", fontsize=9)

fmax = 0.2
m = f <= fmax
for a, Z, col, ttl in ((axes[1, 0], S, C["green"], "(라) 자극의 스펙트럼"),
                       (axes[1, 2], Y, C["red"], "(바) = BOLD의 스펙트럼")):
    Zn = Z[m] / Z[m].max()
    keep = Zn > 1e-3
    a.vlines(f[m][keep], 0, Zn[keep], color=col, lw=1.6)
    a.plot(f[m][keep], Zn[keep], "o", color=col, ms=3)
    a.set_title(ttl, fontsize=9.5)
mh = fh <= fmax
axes[1, 1].plot(fh[mh], H[mh] / H[mh].max(), color=C["blue"])
axes[1, 1].set_title("(마) × HRF의 이득", fontsize=9.5)
for a in axes[1]:
    a.set_xlim(0, fmax)
    a.set_ylim(0, 1.15)
    a.set_xlabel("주파수 (Hz)", fontsize=9)
    a.set_xticks([0, 0.05, 0.1, 0.15, 0.2])
    a.set_xticklabels(["0", ".05", ".1", ".15", ".2"])
axes[1, 0].text(0.034, 0.95, "0.025 Hz", fontsize=7.5, color=C["green"])
axes[1, 0].text(0.085, 0.42, "홀수 배음", fontsize=7.5, color=C["green"])
axes[1, 1].axvline(0.1, color=C["gray"], lw=0.6, ls=":")
axes[1, 1].text(0.105, 0.5, "0.1 Hz에서\n약 0.38", fontsize=7.5)
axes[1, 2].text(0.06, 0.45, "배음이 깎였다", fontsize=7.5, color=C["red"])
for a in axes.flat:
    a.tick_params(labelsize=8)
save(fig, __file__)
