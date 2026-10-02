from figstyle import plt, np, save, C

# sinc RF 펄스(길이 3.125 ms, 시간-대역폭 곱 4) → 대역폭 1.28 kHz → 경사 10 mT/m에서 두께 3.0 mm.
gbar = 42.58e6
T = 3.125e-3
TBW = 4
BW = TBW / T                                # 1280 Hz
dt = 1e-6
t = np.arange(-T / 2, T / 2, dt)
rf = np.sinc(t * BW) * (0.54 + 0.46 * np.cos(2 * np.pi * t / T))   # 해밍 창

n = 2 ** 18
spec = np.abs(np.fft.fftshift(np.fft.fft(rf, n)))
spec /= spec.max()
f = np.fft.fftshift(np.fft.fftfreq(n, dt))

fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.8), gridspec_kw=dict(width_ratios=[1, 1, 1.25], wspace=0.42))
a1, a2, a3 = axs
a1.plot(t * 1e3, rf, color=C["purple"])
a1.axhline(0, color=C["gray"], lw=0.6)
a1.set_xlabel("시간 (ms)")
a1.set_yticks([])
a1.set_title("(가) sinc 모양 RF 펄스", fontsize=10)

a2.plot(f / 1e3, spec, color=C["purple"])
a2.set_xlim(-2, 2)
a2.set_xlabel("주파수 차이 (kHz)")
a2.set_yticks([])
a2.annotate("", xy=(BW / 2e3, 0.5), xytext=(-BW / 2e3, 0.5),
            arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1, shrinkA=0, shrinkB=0))
a2.text(0, 1.04, f"Δf = {BW / 1e3:.2f} kHz", ha="center", fontsize=8.5, color=C["red"])
a2.set_ylim(0, 1.2)
a2.set_title("(나) 그 주파수 성분", fontsize=10)

z = np.linspace(-8, 8, 100)              # mm
for G, col, lab in ((10e-3, C["blue"], "10 mT/m"), (5e-3, C["gray"], "5 mT/m")):
    fz = gbar * G * z * 1e-3 / 1e3       # kHz
    a3.plot(z, fz, color=col, lw=1.8)
    th = BW / (gbar * G) * 1e3           # mm
    a3.fill_betweenx([-BW / 2e3, BW / 2e3], -th / 2, th / 2, color=col, alpha=0.18, lw=0)
    a3.plot([-th / 2, -th / 2], [-3, -BW / 2e3], color=col, ls=":", lw=0.9)
    a3.plot([th / 2, th / 2], [-3, BW / 2e3], color=col, ls=":", lw=0.9)
    if G > 6e-3:
        a3.text(3.9, gbar * G * 4.2e-3 / 1e3 + 0.1, lab, color=col, fontsize=8.5, ha="right", va="bottom")
    else:
        a3.text(7.9, gbar * G * 7.9e-3 / 1e3 - 0.75, lab, color=col, fontsize=8.5, ha="right", va="top")
    print(lab, round(th, 2), "mm")
a3.axhspan(-BW / 2e3, BW / 2e3, color=C["red"], alpha=0.10, lw=0)
a3.text(-7.6, BW / 2e3 + 0.1, "RF 대역", color=C["red"], fontsize=8.5, va="bottom")
a3.annotate("", xy=(1.5, -2.65), xytext=(-1.5, -2.65),
            arrowprops=dict(arrowstyle="<->", color=C["blue"], lw=0.9, shrinkA=0, shrinkB=0, mutation_scale=6))
a3.text(1.9, -2.65, "3.0 mm", ha="left", fontsize=8.5, color=C["blue"], va="center")
a3.annotate("", xy=(3.0, -2.2), xytext=(-3.0, -2.2),
            arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.9, shrinkA=0, shrinkB=0))
a3.text(3.4, -2.2, "6.0 mm", ha="left", fontsize=8.5, color=C["gray"], va="center")
a3.set_ylim(-3, 3.6)
a3.set_xlim(-8, 8)
a3.set_xlabel("슬라이스 방향 위치 z (mm)")
a3.set_ylabel("주파수 차이 (kHz)", fontsize=9)
a3.set_title("(다) 경사: 대역 → 두께", fontsize=10)
save(fig, __file__)
