import sys

from scipy.signal import butter, sosfiltfilt, hilbert

from figstyle import plt, np, save, C

# 위상-진폭 결합(PAC)의 모의실험. 6 Hz 세타의 마루 근처에서 60 Hz 감마 진폭이 커지는 신호와
# 감마 진폭이 세타와 무관한 신호를 만들고(둘 다 1/f 배경 잡음 위), 토르트의 변조 지수
# (MI, Tort 2010)로 비교한다. 표본화 500 Hz, 120 s.
rng = np.random.default_rng(4)
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


def make(coupled):
    th = bp(rng.normal(size=n), 5, 7, 2)                    # 좁은 대역 세타 (위상이 천천히 떠돈다)
    th /= np.abs(hilbert(th)).mean()
    ph = np.angle(hilbert(th))
    theta = th
    mod = (1 + 0.8 * np.cos(ph)) / 1.8 if coupled else 0.55 * np.ones(n)
    gamma = 0.35 * mod * np.cos(2 * np.pi * 60 * t + rng.uniform(0, 2 * np.pi))
    return theta + gamma + pink(0.6)


def tort_mi(phase, amp, nb=18):
    edges = np.linspace(-np.pi, np.pi, nb + 1)
    idx = np.clip(np.digitize(phase, edges) - 1, 0, nb - 1)
    m = np.bincount(idx, weights=amp, minlength=nb) / np.bincount(idx, minlength=nb)
    P = m / m.sum()
    return (np.log(nb) + np.sum(P * np.log(P))) / np.log(nb), P


def como(x, fps, fas):
    phs = [np.angle(hilbert(bp(x, f - 1, f + 1, 2))) for f in fps]
    amps = [np.abs(hilbert(bp(x, f - 10, f + 10))) for f in fas]
    return np.array([[tort_mi(p, a)[0] for p in phs] for a in amps])


if __name__ == "__main__":
    xc, xu = make(True), make(False)
    res = {}
    for key, x in (("coupled", xc), ("uncoupled", xu)):
        ph = np.angle(hilbert(bp(x, 5, 7, 2)))
        am = np.abs(hilbert(bp(x, 50, 70)))
        mi, P = tort_mi(ph, am)
        sh = [tort_mi(ph, np.roll(am, rng.integers(fs * 5, n - fs * 5)))[0] for _ in range(200)]
        res[key] = (mi, P)
        print(f"{key}: MI={mi:.2e}, 시간 이동 대리 95%={np.quantile(sh, 0.95):.2e}, "
              f"최대/최소 bin 비={P.max() / P.min():.2f}", file=sys.stderr)
    fps = np.arange(2, 15, 1.0)
    fas = np.arange(25, 141, 5.0)
    M = como(xc, fps, fas)
    i, j = np.unravel_index(M.argmax(), M.shape)
    print(f"공동변조도 최댓값: 위상 {fps[j]:.0f} Hz, 진폭 {fas[i]:.0f} Hz, MI={M.max():.2e}", file=sys.stderr)

    fig = plt.figure(figsize=(7.4, 3.0))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 0.9, 1.1], hspace=0.3, wspace=0.45)
    seg = (t >= 10) & (t < 10.8)
    a = fig.add_subplot(gs[0, 0])
    a.plot(t[seg] - 10, xc[seg], color=C["gray"], lw=0.6)
    a.plot(t[seg] - 10, bp(xc, 5, 7, 2)[seg], color=C["blue"], lw=1.5)
    a.set_xticklabels([])
    a.set_yticks([])
    a.spines["left"].set_visible(False)
    a.set_title("(가) 세타 마루에 감마가 실린다", fontsize=9.5, pad=14)
    a.text(0.0, 1.0, "원신호와 세타(5–7 Hz)", transform=a.transAxes, fontsize=7.5, color=C["blue"], va="bottom")
    a2 = fig.add_subplot(gs[1, 0])
    g = bp(xc, 50, 70)
    a2.plot(t[seg] - 10, g[seg], color=C["red"], lw=0.6)
    a2.plot(t[seg] - 10, np.abs(hilbert(g))[seg], color=C["red"], lw=1.5)
    a2.set_yticks([])
    a2.spines["left"].set_visible(False)
    a2.set_xlabel("시간 (s)")
    a2.text(0.0, 1.02, "감마(50–70 Hz)와 그 포락선", transform=a2.transAxes, fontsize=7.5, color=C["red"],
            va="bottom")

    b = fig.add_subplot(gs[:, 1])
    centers = np.degrees(np.linspace(-np.pi, np.pi, 19)[:-1] + np.pi / 18)
    b.plot(centers, res["coupled"][1], "o-", color=C["blue"], ms=3, lw=1.4, label="결합")
    b.plot(centers, res["uncoupled"][1], "s-", color=C["red"], ms=3, lw=1.2, mfc="white", label="무결합")
    b.axhline(1 / 18, color=C["gray"], lw=0.6, ls=":")
    b.set_xlim(-180, 180)
    b.set_xticks([-180, -90, 0, 90, 180])
    b.set_xticklabels(["−180", "", "0", "", "180"])
    b.set_ylim(0.02, 0.095)
    b.set_xlabel("세타 위상 (°, 0 = 마루)")
    b.set_ylabel("감마 진폭 분포 P")
    b.legend(fontsize=7.3, loc="upper left")
    b.text(0, 0.023, f"MI: {res['coupled'][0] * 1e3:.1f} 대 {res['uncoupled'][0] * 1e3:.2f} (×10⁻³)",
           ha="center", fontsize=6.8, color=C["ink"])
    b.set_title("(나) 위상별 진폭", fontsize=9.5)

    c = fig.add_subplot(gs[:, 2])
    im = c.imshow(M * 1e3, origin="lower", aspect="auto", cmap="Blues",
                  extent=[fps[0] - 0.5, fps[-1] + 0.5, fas[0] - 2.5, fas[-1] + 2.5])
    cb = fig.colorbar(im, ax=c, fraction=0.06, pad=0.03)
    cb.set_label("MI (×10⁻³)", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    c.set_xlabel("위상 주파수 (Hz)")
    c.set_ylabel("진폭 주파수 (Hz)")
    c.set_title("(다) 공동변조도", fontsize=9.5)
    save(fig, __file__)
