from figstyle import plt, np, save, C

# 피크 진폭과 평균 진폭: 시행 수가 적을수록 피크 진폭은 위로 치우친다.
fs = 500
t = np.arange(-0.2, 0.8, 1 / fs)
true = 8.0 * np.exp(-0.5 * ((t - 0.350) / 0.060) ** 2)   # P3만 남긴 단순 ERP
rng = np.random.default_rng(7)
nt = len(t)
f = np.fft.rfftfreq(nt, 1 / fs)
amp = np.zeros_like(f)
amp[1:] = 1 / np.sqrt(f[1:])


def noise(shape, sd=20.0):
    X = (rng.standard_normal(shape + (len(f),)) + 1j * rng.standard_normal(shape + (len(f),))) * amp
    x = np.fft.irfft(X, nt, axis=-1)
    return x / x.std(axis=-1, keepdims=True) * sd


search = (t >= 0.250) & (t <= 0.500)     # 피크를 찾는 창
mwin = (t >= 0.300) & (t <= 0.400)       # 평균 진폭 창
peak_true = true[search].max()
mean_true = true[mwin].mean()

fig, axs = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(wspace=0.32, width_ratios=[1.05, 1]))
ax = axs[0]
avg = true + noise((20,)).mean(0)
ax.axvspan(250, 500, color=C["light"], zorder=0)
ax.axvspan(300, 400, color="#d6e2f0", zorder=0)
ax.plot(t * 1000, avg, color=C["blue"], lw=1.0, label="20시행 평균")
ax.plot(t * 1000, true, color=C["red"], lw=1.0, ls="--", label="참 ERP")
ip = np.where(search)[0][avg[search].argmax()]
ax.scatter([t[ip] * 1000], [avg[ip]], color=C["red"], s=22, zorder=4)
ax.annotate(f"피크 {avg[ip]:.1f} μV\n({t[ip] * 1000:.0f} ms)", xy=(t[ip] * 1000, avg[ip]), xytext=(510, 12.5),
            fontsize=7.8, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6), va="center")
mv = avg[mwin].mean()
ax.plot([300, 400], [mv, mv], color=C["ink"], lw=2)
ax.annotate(f"평균 진폭 {mv:.1f} μV", xy=(400, mv), xytext=(470, -6.5), fontsize=7.8, bbox=dict(facecolor="white", edgecolor="none", pad=0.6),
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6), va="center")
ax.text(375, 17.6, "피크 탐색 창", fontsize=7, ha="center", color=C["gray"])
ax.text(350, 16.0, "평균 창", fontsize=7, ha="center", color=C["blue"])
ax.axhline(0, color=C["gray"], lw=0.6)
ax.set_xlim(-200, 800)
ax.set_ylim(-13.5, 19.5)
ax.set_xlabel("자극 뒤 시간 (ms)")
ax.set_ylabel("전위 (μV)")
ax.legend(fontsize=7.5, loc="upper left")
ax.set_title("(가) 한 사람의 20시행 평균", fontsize=10)

ax = axs[1]
Ns = np.array([10, 20, 40, 80, 160, 320])
reps = 1500
pb, ps, mb, ms = [], [], [], []
for n in Ns:
    avgs = true + noise((reps,)) / np.sqrt(n)    # n시행 평균의 잡음은 1/√n
    pk = avgs[:, search].max(1) - peak_true
    mn = avgs[:, mwin].mean(1) - mean_true
    pb.append(pk.mean()); ps.append(pk.std())
    mb.append(mn.mean()); ms.append(mn.std())
pb, ps, mb, ms = map(np.array, (pb, ps, mb, ms))
x = np.arange(len(Ns))
ax.errorbar(x - 0.08, pb, yerr=ps, color=C["red"], marker="o", ms=4, lw=1.2, capsize=2, label="피크 진폭")
ax.errorbar(x + 0.08, mb, yerr=ms, color=C["blue"], marker="s", ms=4, lw=1.2, capsize=2, label="평균 진폭")
ax.axhline(0, color=C["gray"], lw=0.8, ls="--")
ax.set_xticks(x)
ax.set_xticklabels([str(n) for n in Ns])
ax.set_xlabel("평균한 시행 수")
ax.set_ylabel("추정값 − 참값 (μV)")
ax.legend(fontsize=7.5, loc="upper right")
ax.set_title("(나) 피크는 위로 치우친다", fontsize=10)
ax.set_ylim(-6, 17)
print("peak bias", np.round(pb, 2), "sd", np.round(ps, 2))
print("mean bias", np.round(mb, 2), "sd", np.round(ms, 2))
print("peak_true", peak_true, "mean_true", round(mean_true, 2))
save(fig, __file__)
