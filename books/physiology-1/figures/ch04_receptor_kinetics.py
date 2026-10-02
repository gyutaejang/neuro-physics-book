from figstyle import plt, np, save, C

t = np.logspace(-1, np.log10(3000), 3000)  # ms


def dexp(t, t0, tr, td):
    s = np.clip(t - t0, 0, None)
    y = (np.exp(-s / td) - np.exp(-s / tr)) * (t >= t0)
    return y / y.max()


curves = [
    (dexp(t, 0.3, 0.3, 2.0), C["blue"], "AMPA\n(감쇠 약 2 ms)", (0.62, 0.92, "right")),
    (dexp(t, 0.3, 0.5, 10.0), C["green"], "GABA-A\n(약 10 ms)", (2.6, 1.04, "center")),
    (dexp(t, 0.5, 6.0, 80.0), C["red"], "NMDA\n(약 50–100 ms)", (17, 1.04, "center")),
    (dexp(t, 20, 60, 250.0), C["purple"], "GABA-B: GPCR\n→ K⁺ 통로 (수백 ms)", (130, 1.04, "center")),
]
fig, ax = plt.subplots(figsize=(6.6, 3.1))
for y, col, lab, (xl, yl, ha) in curves:
    ls = "--" if "GPCR" in lab else "-"
    ax.plot(t, y, color=col, lw=1.7, ls=ls)
    ax.text(xl, yl, lab, color=col, fontsize=8, ha=ha, va="bottom" if ha == "center" else "center")
ax.set_xscale("log")
ax.set_xlim(0.1, 3000)
ax.set_ylim(0, 1.45)
ax.set_xticks([0.1, 1, 10, 100, 1000])
ax.set_xticklabels(["0.1", "1", "10", "100", "1000"])
ax.set_xlabel("전달물질 방출 뒤 시간 (ms, 로그 눈금)")
ax.set_ylabel("시냅스 전류 (봉우리 = 1)")
ax.text(0.12, 1.36, "이온성: 1 ms 안에 열린다", fontsize=8, va="center", color=C["ink"])
ax.text(2900, 1.36, "대사성: 수십 ms 뒤 시작", fontsize=8, va="center", ha="right", color=C["ink"])
save(fig, __file__)
