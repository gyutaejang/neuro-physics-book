from figstyle import plt, np, save, C

rng = np.random.default_rng(5)
fs = 500


def bg(n, rms):
    f = np.fft.rfftfreq(n, 1 / fs)
    spec = np.zeros_like(f)
    m = (f > 0.5) & (f < 35)
    spec[m] = 1 / f[m] ** 0.7
    x = np.fft.irfft(spec * np.exp(2j * np.pi * rng.random(f.size)), n=n)
    return x / x.std() * rms


def spike(t, t0, a_sp, a_w):
    """표면 음성(−) 값을 양수로 돌려준다(그림은 임상 관례대로 위가 음)."""
    return (a_sp * np.exp(-0.5 * ((t - t0) / 0.011) ** 2)
            - 0.25 * a_sp * np.exp(-0.5 * ((t - t0 - 0.04) / 0.02) ** 2)
            + a_w * np.exp(-0.5 * ((t - t0 - 0.17) / 0.06) ** 2))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.8), gridspec_kw=dict(width_ratios=[1, 2.2]))

# (가) 발작 사이 극파 하나
t = np.arange(-0.4, 0.8, 1 / fs)
y = bg(t.size, 12) - spike(t, 0.0, 140, 60)
a1.plot(t * 1000, y, color=C["blue"], lw=1.0)
a1.axvspan(-25, 25, color=C["light"], lw=0)
a1.text(45, -150, "극파 (폭 약 50 ms)", ha="left", va="center", fontsize=7.5, color=C["red"])
a1.text(260, -95, "뒤따르는 서파", ha="left", va="center", fontsize=7.5, color=C["gray"])
a1.set_ylim(-200, 80)
a1.set_xlabel("시간 (ms)")
a1.set_ylabel("전위 (μV, 위가 음)")
a1.set_title("(가) 발작 사이 극파", fontsize=10)

# (나) 3 Hz 극서파 (소발작)
T = 8.0
t = np.arange(0, T, 1 / fs)
y = bg(t.size, 15)
on, off = 2.0, 6.0
for t0 in np.arange(on, off, 1 / 3.0):
    ramp = min(1.0, (t0 - on) / 0.4 + 0.5)
    y -= spike(t, t0, 300 * ramp, 220 * ramp)
a2.plot(t, y, color=C["blue"], lw=0.8)
a2.axvspan(on, off, color=C["light"], lw=0, zorder=0)
a2.text((on + off) / 2, -400, "약 3 Hz 극서파가 수 초 이어지는 동안 의식이 잠깐 끊긴다", ha="center", va="center",
        fontsize=8, color=C["red"])
a2.annotate("", xy=(on + 1, 150), xytext=(on, 150), arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.8))
a2.text(on + 0.5, 185, "1 s에 3번", ha="center", va="center", fontsize=7.5, color=C["gray"])
a2.set_ylim(-450, 220)
a2.set_xlim(0, T)
a2.set_xlabel("시간 (s)")
a2.set_title("(나) 소발작의 3 Hz 극서파 (모식도)", fontsize=10)
for a in (a1, a2):
    a.invert_yaxis()
fig.tight_layout()
save(fig, __file__)
