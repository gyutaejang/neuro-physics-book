from figstyle import plt, np, save, C

t = np.linspace(-1, 8, 2000)  # ms, 0 = 시냅스 앞 활동전위 봉우리


def gauss(t, m, s):
    return np.exp(-0.5 * ((t - m) / s) ** 2)


def dexp(t, t0, tr, td):
    s = np.clip(t - t0, 0, None)
    y = (np.exp(-s / td) - np.exp(-s / tr)) * (t >= t0)
    return y / y.max()


ap = -70 + 100 * np.where(t < 0, gauss(t, 0, 0.18), gauss(t, 0, 0.3))
ica = gauss(t, 0.35, 0.12)
rel = np.where(t < 0.5, gauss(t, 0.5, 0.07), gauss(t, 0.5, 0.15))
epsc = dexp(t, 0.55, 0.25, 2.0)
epsp = dexp(t, 0.6, 1.2, 15.0)

fig, axs = plt.subplots(5, 1, figsize=(6.2, 4.6), sharex=True,
                        gridspec_kw=dict(hspace=0.25))
rows = [
    (ap, C["blue"], "① 시냅스 앞\n활동전위", None),
    (ica, C["red"], "② Ca²⁺ 유입", None),
    (rel, C["green"], "③ 소포 융합\n(방출 속도)", None),
    (-epsc, C["purple"], "④ 시냅스 후\n전류 (EPSC)", None),
    (epsp, C["blue"], "⑤ 시냅스 후\n전위 (EPSP)", None),
]
for ax, (y, col, lab, _) in zip(axs, rows):
    ax.plot(t, y, color=col, lw=1.6)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(-1.25, (y.max() + y.min()) / 2, lab, ha="right", va="center", fontsize=8.5)
    ax.axvline(0, color=C["gray"], lw=0.5, ls=":")
    ax.axvline(0.55, color=C["gray"], lw=0.5, ls=":")
axs[0].text(-0.2, 25, "+30 mV", ha="right", fontsize=7.5, color=C["gray"], va="center")
axs[1].text(1.0, 0.6, "활동전위가 내려오는\n동안 열린다", fontsize=7.5, color=C["gray"], va="center")
axs[2].text(1.0, 0.6, "Ca²⁺ 유입 뒤\n0.1–0.2 ms", fontsize=7.5, color=C["gray"], va="center")
axs[3].text(3.2, -0.8, "AMPA 전류: 수 ms에 끝난다", fontsize=7.5, color=C["gray"], va="center")
axs[4].text(3.0, 0.45, "막 시간 상수 때문에 수십 ms 이어진다", fontsize=7.5, color=C["gray"], va="center")
axs[0].annotate("", xy=(0.55, -55), xytext=(0, -55),
                arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.0, mutation_scale=8))
axs[0].text(0.65, -50, "시냅스 지연 약 0.5 ms", fontsize=8, color=C["red"], va="center")
axs[-1].set_xlabel("시간 (ms, 0 = 시냅스 앞 활동전위 봉우리)")
axs[-1].set_xlim(-1, 8)
save(fig, __file__)
