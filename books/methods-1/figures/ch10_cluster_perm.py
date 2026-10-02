from figstyle import plt, np, save, C
from scipy import stats
from scipy.ndimage import gaussian_filter1d

# 시간 축 군집 기반 순열 검정. 참가자 20명의 차이파(조건 A − B), 효과는 300–500 ms에만 있다.
fs = 250
t = np.arange(-0.2, 0.8, 1 / fs)
nsub = 20
rng = np.random.default_rng(11)
effect = 1.6 * np.exp(-0.5 * ((t - 0.400) / 0.060) ** 2)
noise = gaussian_filter1d(rng.standard_normal((nsub, len(t))), sigma=5, axis=1)
noise = noise / noise.std() * 2.5
diff = effect + noise


def tvals(d):
    return d.mean(0) / (d.std(0, ddof=1) / np.sqrt(d.shape[0]))


def clusters(tv, thr):
    """문턱을 넘는 이웃 시점 묶음과 그 t 합(군집 질량)."""
    out = []
    for sign in (1, -1):
        above = sign * tv > thr
        i = 0
        while i < len(tv):
            if above[i]:
                j = i
                while j + 1 < len(tv) and above[j + 1]:
                    j += 1
                out.append((i, j, tv[i:j + 1].sum()))
                i = j + 1
            else:
                i += 1
    return out


thr = stats.t.ppf(0.975, nsub - 1)
tv = tvals(diff)
obs = clusters(tv, thr)
nperm = 2000
null = np.empty(nperm)
for k in range(nperm):
    flips = rng.choice([-1, 1], size=(nsub, 1))
    cl = clusters(tvals(diff * flips), thr)
    null[k] = max([abs(c[2]) for c in cl], default=0.0)
crit = np.quantile(null, 0.95)

fig, axs = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(wspace=0.32, width_ratios=[1.35, 1]))
ax = axs[0]
ax.plot(t * 1000, tv, color=C["blue"], lw=1.2)
ax.axhline(thr, color=C["gray"], lw=0.8, ls="--")
ax.axhline(-thr, color=C["gray"], lw=0.8, ls="--")
ax.axhline(0, color=C["gray"], lw=0.5)
ax.text(795, -thr - 0.3, f"군집 형성 문턱 |t| = {thr:.2f}", fontsize=7.5, color=C["gray"], ha="right", va="top")
for i, j, m in obs:
    p = (np.sum(null >= abs(m)) + 1) / (nperm + 1)
    col = C["red"] if p < 0.05 else C["purple"]
    ax.fill_between(t[i:j + 1] * 1000, 0, tv[i:j + 1], color=col, alpha=0.35, lw=0)
    xm = t[(i + j) // 2] * 1000
    ym = tv[i:j + 1].max() if m > 0 else tv[i:j + 1].min()
    ptxt = "p < 0.001" if p < 0.001 else f"p = {p:.2f}"
    ha = "center"
    if xm < -120:
        xm, ha = -195, "left"
    ax.text(xm, ym + (0.35 if m > 0 else -0.35), f"질량 {m:.0f}\n{ptxt}", fontsize=7.3, ha=ha,
            va="bottom" if m > 0 else "top", color=col)
    print(f"cluster {t[i]*1000:.0f}-{t[j]*1000:.0f} ms mass {m:.1f} p {p:.4f}")
ax.set_xlim(-200, 800)
ax.set_ylim(-5, 8.2)
ax.set_xlabel("자극 뒤 시간 (ms)")
ax.set_ylabel("t 값 (자유도 19)")
ax.set_title("(가) 시점마다 t, 문턱을 넘는 군집", fontsize=10)

ax = axs[1]
ax.hist(null, bins=40, color=C["gray"], alpha=0.7)
ax.axvline(crit, color=C["ink"], lw=1, ls="--")
ax.text(crit + 3, ax.get_ylim()[1] * 0.92, f"95번째 백분위\n= {crit:.0f}", fontsize=7.5, va="top",
        bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
for i, j, m in obs:
    p = (np.sum(null >= abs(m)) + 1) / (nperm + 1)
    ax.axvline(abs(m), color=C["red"] if p < 0.05 else C["purple"], lw=1.6)
ax.set_xlabel("순열마다 가장 큰 군집 질량")
ax.set_ylabel("순열 횟수")
ax.set_title(f"(나) 귀무 분포 ({nperm}번 부호 뒤집기)", fontsize=10)
n_unc = int(np.sum(np.abs(tv) > thr))
print("thr", thr, "crit", crit, "n points above", n_unc, "of", len(t))
save(fig, __file__)
