import sys

from scipy.signal import butter, sosfiltfilt, hilbert, sawtooth, welch

from figstyle import plt, np, save, C

# 가짜 PAC. 감마 진동이 전혀 없는, 날카로운 톱니 모양의 8 Hz 리듬(천천히 내려가다 약 6 ms 만에
# 되돌아온다)에 1/f 잡음만 더했다. 고조파(16, 24, … Hz)가 감마 대역까지 이어지고,
# 감마 대역 필터는 날카로운 모서리마다 짧게 울려 위상에 묶인 '진폭'을 만든다.
rng = np.random.default_rng(8)
fs, dur = 500, 120
n = fs * dur
t = np.arange(n) / fs
fr = np.fft.rfftfreq(n, 1 / fs)


def pink(scale):
    X = np.fft.rfft(rng.normal(size=n)) / np.maximum(fr, 1) ** 0.5
    x = np.fft.irfft(X, n)
    return scale * x / x.std()


def bp(x, lo, hi, order=3):
    return sosfiltfilt(butter(order, [lo, hi], btype="band", fs=fs, output="sos"), x)


def tort_mi(phase, amp, nb=18):
    edges = np.linspace(-np.pi, np.pi, nb + 1)
    idx = np.clip(np.digitize(phase, edges) - 1, 0, nb - 1)
    m = np.bincount(idx, weights=amp, minlength=nb) / np.bincount(idx, minlength=nb)
    P = m / m.sum()
    return (np.log(nb) + np.sum(P * np.log(P))) / np.log(nb)


slowf = np.fft.irfft(np.fft.rfft(rng.normal(size=n)) * (fr < 0.5), n)
f_inst = 8 + 0.3 * slowf / slowf.std()
phi = 2 * np.pi * np.cumsum(f_inst) / fs
wave = -sawtooth(phi, width=0.95)        # 천천히 내려가고, 주기의 5 %(약 6 ms) 동안 빠르게 올라간다
x = wave + pink(0.25)

fps = np.arange(2, 15, 1.0)
fas = np.arange(25, 141, 5.0)
phs = [np.angle(hilbert(bp(x, f - 1, f + 1, 2))) for f in fps]
M = np.array([[tort_mi(p, np.abs(hilbert(bp(x, fa - 10, fa + 10)))) for p in phs] for fa in fas])
i, j = np.unravel_index(M.argmax(), M.shape)
ph8 = np.angle(hilbert(bp(x, 7, 9, 2)))
mi60 = tort_mi(ph8, np.abs(hilbert(bp(x, 50, 70))))
print(f"최댓값: 위상 {fps[j]:.0f} Hz, 진폭 {fas[i]:.0f} Hz, MI={M.max():.2e}; 8 Hz–60 Hz MI={mi60:.2e}",
      file=sys.stderr)
print("진폭 주파수별 8 Hz MI:", dict(zip(fas[::3], np.round(M[::3, list(fps).index(8)] * 1e3, 2))),
      file=sys.stderr)

fig = plt.figure(figsize=(7.4, 3.0))
gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 0.95, 1.1], hspace=0.3, wspace=0.45)
seg = (t >= 20) & (t < 20.6)
a = fig.add_subplot(gs[0, 0])
a.plot(t[seg] - 20, x[seg], color=C["gray"], lw=0.7)
a.plot(t[seg] - 20, wave[seg], color=C["blue"], lw=1.4)
a.set_xticklabels([])
a.set_yticks([])
a.spines["left"].set_visible(False)
a.set_title("(가) 감마 없는 날카로운 리듬", fontsize=9.5, pad=14)
a.text(0.0, 1.0, "원신호와 톱니 모양 8 Hz 성분", transform=a.transAxes, fontsize=7.5, color=C["blue"],
       va="bottom")
a2 = fig.add_subplot(gs[1, 0])
g = bp(x, 50, 70)
a2.plot(t[seg] - 20, g[seg], color=C["red"], lw=0.7)
a2.plot(t[seg] - 20, np.abs(hilbert(g))[seg], color=C["red"], lw=1.4)
a2.set_yticks([])
a2.spines["left"].set_visible(False)
a2.set_xlabel("시간 (s)")
a2.text(0.0, 1.0, "50–70 Hz 필터 출력과 포락선", transform=a2.transAxes, fontsize=7.5,
        color=C["red"], va="bottom")

b = fig.add_subplot(gs[:, 1])
f, P = welch(x, fs=fs, nperseg=fs * 4)
fw, Pw = welch(pink(0.25), fs=fs, nperseg=fs * 4)
b.semilogy(fw, Pw, color=C["gray"], lw=0.9, label="1/f 잡음만")
b.semilogy(f, P, color=C["blue"], lw=1.0, label="원신호")
b.set_xlim(0, 100)
b.set_ylim(1e-5, 1)
b.set_xlabel("주파수 (Hz)")
b.set_ylabel("파워 (상대)")
b.legend(fontsize=7.3, loc="upper right")
b.set_title("(나) 고조파가 감마까지", fontsize=9.5)

c = fig.add_subplot(gs[:, 2])
im = c.imshow(M * 1e3, origin="lower", aspect="auto", cmap="Blues",
              extent=[fps[0] - 0.5, fps[-1] + 0.5, fas[0] - 2.5, fas[-1] + 2.5])
cb = fig.colorbar(im, ax=c, fraction=0.06, pad=0.03)
cb.set_label("MI (×10⁻³)", fontsize=8)
cb.ax.tick_params(labelsize=7)
c.set_xlabel("위상 주파수 (Hz)")
c.set_ylabel("진폭 주파수 (Hz)")
c.set_title("(다) 넓게 번진 가짜 결합", fontsize=9.5)
save(fig, __file__)
