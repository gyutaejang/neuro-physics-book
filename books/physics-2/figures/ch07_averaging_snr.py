from figstyle import plt, np, save, C

# 평균과 SNR: 시행마다 같은 ERP(정점 5 μV)에 시행마다 다른 잡음(표준편차 20 μV, 백색으로 단순화)이 더해진다.
rng = np.random.default_rng(7)
fs = 250
t = np.arange(-0.2, 0.8, 1 / fs)
erp = 5 * np.exp(-((t - 0.35) / 0.08) ** 2)          # P300 모양의 양성 봉우리 (μV)
sd = 20.0
trials = erp + rng.normal(0, sd, (400, len(t)))

fig = plt.figure(figsize=(7.4, 3.3))
gs = fig.add_gridspec(3, 2, width_ratios=[1.35, 1], hspace=0.25, wspace=0.32)
for row, n in enumerate((1, 16, 144)):
    ax = fig.add_subplot(gs[row, 0])
    avg = trials[:n].mean(axis=0)
    ax.plot(t * 1000, avg, color=C["blue"], lw=0.9)
    ax.plot(t * 1000, erp, color=C["red"], lw=1.2, ls="--")
    lim = 3 * sd / np.sqrt(n) + 6
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color=C["gray"], lw=0.5)
    ax.set_xlim(-200, 800)
    ax.tick_params(labelsize=7.5)
    ax.text(0.01, 0.97, f"{n}회 평균: 잡음 {sd / np.sqrt(n):.1f} μV", transform=ax.transAxes,
            fontsize=8, va="top", bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    if row < 2:
        ax.set_xticklabels([])
    if row == 0:
        ax.set_title("(가) 시행을 평균하면 ERP가 드러난다", fontsize=9.5)
        ax.text(0.99, 0.97, "빨간 점선: 실제 ERP", transform=ax.transAxes, fontsize=7.5,
                ha="right", va="top", color=C["red"], bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    if row == 1:
        ax.set_ylabel("전위 (μV)", fontsize=9)
ax.set_xlabel("자극 뒤 시간 (ms)", fontsize=9)

ax = fig.add_subplot(gs[:, 1])
ns = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256])
i0 = np.argmin(abs(t - 0.35))
base = t < 0
snr = []
for n in ns:
    vals = []
    for r in range(40):
        idx = rng.choice(400, n, replace=False)
        avg = trials[idx].mean(axis=0)
        vals.append(erp[i0] / avg[base].std())
    snr.append(np.mean(vals))
ax.loglog(ns, snr, "o", color=C["blue"], ms=4, label="모의 실험")
ax.loglog(ns, 0.25 * np.sqrt(ns), color=C["red"], lw=1.2, label="0.25 × √N")
ax.axhline(3, color=C["gray"], lw=0.6, ls=":")
ax.text(1.1, 3.25, "SNR = 3 (N = 144)", fontsize=7.5, color=C["gray"])
ax.set_xlabel("평균한 시행 수 N", fontsize=9)
ax.set_ylabel("SNR (정점 / 잡음 표준편차)", fontsize=9)
ax.set_xticks([1, 4, 16, 64, 256])
ax.set_xticklabels(["1", "4", "16", "64", "256"])
ax.set_yticks([0.25, 0.5, 1, 2, 4])
ax.set_yticklabels(["0.25", "0.5", "1", "2", "4"])
ax.minorticks_off()
ax.legend(fontsize=7.5, loc="lower right")
ax.set_title("(나) SNR은 √N으로 는다", fontsize=9.5)
save(fig, __file__)
