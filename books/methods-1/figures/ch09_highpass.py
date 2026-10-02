from scipy import signal

from figstyle import plt, np, save, C

# 합성 ERP: P1, N1, 그리고 느리고 큰 양전위(P3/후기 양전위 같은 성분).
fs = 250.0
t = np.arange(-5, 5, 1 / fs)


def g(mu, sd, a):
    return a * np.exp(-0.5 * ((t - mu) / sd) ** 2)


erp = g(0.10, 0.015, 2) + g(0.17, 0.02, -4) + g(0.50, 0.17, 8)


def hp(x, fc):
    b, a = signal.butter(2, fc, "high", fs=fs)
    return signal.filtfilt(b, a, x)


ms = t * 1000
fig = plt.figure(figsize=(7.3, 3.0))
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1], wspace=0.3)

a1 = fig.add_subplot(gs[0, 0])
a1.axhline(0, color=C["gray"], lw=0.5)
a1.axvline(0, color=C["gray"], lw=0.5, ls=":")
a1.axvspan(300, 700, color=C["light"], zorder=0)
a1.plot(ms, erp, color=C["gray"], lw=2.2, alpha=0.7, label="원래")
styles = [(0.1, C["blue"], "-"), (0.5, C["purple"], "-"), (1.0, C["red"], "-"), (2.0, C["red"], ":")]
for fc, col, ls in styles:
    a1.plot(ms, hp(erp, fc), color=col, lw=1.3, ls=ls, label=f"{fc:g} Hz")
a1.text(310, 9.0, "평균 진폭 창", fontsize=7.5, color=C["gray"])
a1.annotate("가짜 음전위", xy=(1000, -1.15), xytext=(820, -4.2), fontsize=7.8, color=C["red"],
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
a1.annotate("N1이 커진다", xy=(170, -5.1), xytext=(-180, -6.6), fontsize=7.8, color=C["purple"],
            arrowprops=dict(arrowstyle="-", color=C["purple"], lw=0.6))
a1.set_xlim(-200, 1200)
a1.set_ylim(-7.5, 10)
a1.set_xlabel("자극 뒤 시간 (ms)")
a1.set_ylabel("전위 (μV)")
a1.set_title("(가) 고역 통과 차단 주파수별 ERP", fontsize=9.5)
a1.legend(fontsize=7.3, loc="upper right", ncol=1)

a2 = fig.add_subplot(gs[0, 1])
fcs = np.logspace(-2, np.log10(3), 60)
w = (t >= 0.3) & (t <= 0.7)
base = erp[w].mean()
amp = [hp(erp, f)[w].mean() / base * 100 for f in fcs]
a2.plot(fcs, amp, color=C["blue"], lw=1.8)
for f in [0.1, 0.5, 1.0]:
    v = hp(erp, f)[w].mean() / base * 100
    a2.scatter([f], [v], s=18, color=C["red"], zorder=3)
    a2.text(f * 1.15, v + 4, f"{f:g} Hz: {v:.0f}%", fontsize=7.8)
a2.set_xscale("log")
a2.set_xticks([0.01, 0.1, 1])
a2.set_xticklabels(["0.01", "0.1", "1"])
a2.set_ylim(0, 108)
a2.set_xlabel("고역 통과 차단 주파수 (Hz)")
a2.set_ylabel("300–700 ms 평균 진폭 (원래 = 100%)")
a2.set_title("(나) 느린 성분이 남는 비율", fontsize=9.5)

save(fig, __file__)
