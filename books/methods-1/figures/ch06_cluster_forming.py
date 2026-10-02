from scipy import ndimage

from figstyle import plt, np, save, C

# 집단 z 지도(128×128, FWHM 6픽셀). 가까운 두 봉우리와 넓고 약한 언덕 하나를 심었다.
L, FW, NSIM = 128, 6.0, 1000
rng = np.random.default_rng(64)
s = FW / np.sqrt(8 * np.log(2))
d = np.zeros((L, L))
d[0, 0] = 1
norm = np.sqrt((ndimage.gaussian_filter(d, s, mode="wrap") ** 2).sum())


def null():
    return ndimage.gaussian_filter(rng.standard_normal((L, L)), s, mode="wrap") / norm


yy, xx = np.mgrid[0:L, 0:L]
blob = lambda cy, cx, w, a: a * np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * w ** 2))
signal = blob(84, 34, 5, 3.8) + blob(84, 48, 5, 3.8) + blob(36, 86, 12, 2.0)
z = null() + signal

cdts = [(2.3, "(가) 군집 형성 문턱 z > 2.3"), (3.1, "(나) 군집 형성 문턱 z > 3.1")]
kcrit = {}
maxsize = {}
for c, _ in cdts:
    mx = np.empty(NSIM)
    for i in range(NSIM):
        lab, n = ndimage.label(null() > c)
        mx[i] = np.bincount(lab.ravel())[1:].max() if n else 0
    maxsize[c] = mx
    kcrit[c] = np.quantile(mx, 0.95)

fig = plt.figure(figsize=(7.4, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.95], wspace=0.18)
for j, (c, title) in enumerate(cdts):
    ax = fig.add_subplot(gs[0, j])
    ax.imshow(z, cmap="Greys", vmin=-5, vmax=5, origin="lower")
    lab, n = ndimage.label(z > c)
    sizes = np.bincount(lab.ravel())
    over = np.zeros((L, L, 4))
    nsurv = 0
    for q in range(1, n + 1):
        if sizes[q] >= kcrit[c]:
            over[lab == q] = [0.15, 0.39, 0.66, 0.9]
            nsurv += 1
            cy, cx = ndimage.center_of_mass(lab == q)
            ax.text(cx, cy + np.sqrt(sizes[q]) * 0.65 + 4, f"{sizes[q]}", color=C["blue"],
                    fontsize=8, ha="center", va="bottom",
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.6, alpha=0.8))
        else:
            over[lab == q] = [0.76, 0.25, 0.05, 0.6]
    ax.imshow(over, origin="lower")
    ax.contour(signal > 1.0, levels=[0.5], colors=[C["green"]], linewidths=0.9, origin="lower")
    ax.set_title(title, fontsize=9)
    ax.text(0.5, -0.04, f"임계 크기 {kcrit[c]:.0f}픽셀, 살아남은 군집 {nsurv}개",
            transform=ax.transAxes, ha="center", va="top", fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color(C["gray"])

a = fig.add_subplot(gs[0, 2])
bins = np.logspace(0, 3.5, 50)
for c, col in [(2.3, C["purple"]), (3.1, C["blue"])]:
    a.hist(maxsize[c], bins=bins, color=col, alpha=0.6, label=f"z > {c}")
    a.axvline(kcrit[c], color=col, lw=1.2, ls="--")
    a.text(kcrit[c] * 1.1, a.get_ylim()[1] * (0.9 if c == 2.3 else 0.75), f"95 %: {kcrit[c]:.0f}",
           fontsize=8, color=col, va="top", bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
a.set_xscale("log")
a.set_xlabel("귀무 지도의 최대 군집 크기 (픽셀)", fontsize=8.5)
a.set_yticks([])
a.set_title("(다) 최대 군집 크기의 귀무 분포", fontsize=9)
a.legend(fontsize=8, loc="center right")
a.set_xticks([1, 10, 100, 1000])
a.set_xticklabels(["1", "10", "100", "1000"])
a.minorticks_off()
save(fig, __file__)
