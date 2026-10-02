from scipy import ndimage, stats

from figstyle import plt, np, save, C

# ch06_permutation_maxstat.py와 같은 합성 데이터(같은 씨앗)를 쓴다.
L, N, FW, NPERM = 96, 20, 6.0, 2000
rng = np.random.default_rng(63)
s = FW / np.sqrt(8 * np.log(2))
d = np.zeros((L, L))
d[0, 0] = 1
norm = np.sqrt((ndimage.gaussian_filter(d, s, mode="wrap") ** 2).sum())
noise = np.stack([ndimage.gaussian_filter(rng.standard_normal((L, L)), s, mode="wrap") / norm
                  for _ in range(N)])
yy, xx = np.mgrid[0:L, 0:L]
blob = lambda cy, cx, w, a: a * np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * w ** 2))
signal = blob(30, 30, 6, 1.5) + blob(66, 64, 3.5, 2.0) + blob(70, 24, 4.5, 1.0)
truth = signal > 0.1
X = noise + signal


def tmap(Y):
    return Y.mean(0) / (Y.std(0, ddof=1) / np.sqrt(N))


T = tmap(X)
maxT = np.empty(NPERM)
for i in range(NPERM):
    maxT[i] = tmap(X * rng.choice([-1.0, 1.0], N)[:, None, None]).max()
m = L * L
p = stats.t.sf(T, N - 1)
ps = np.sort(p.ravel())
rank = np.arange(1, m + 1)
ok = np.nonzero(ps <= 0.05 * rank / m)[0]
p_fdr = ps[ok.max()] if ok.size else 0.0
masks = {
    "unc": p < 0.001,
    "bonf": p < 0.05 / m,
    "perm": T > np.quantile(maxT, 0.95),
    "fdr": p <= p_fdr,
}

fig = plt.figure(figsize=(7.2, 5.0))
gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.3)


def show(ax, mask, title):
    ax.imshow(T, cmap="Greys", vmin=-6, vmax=6, origin="lower")
    over = np.zeros((L, L, 4))
    if mask is None:
        over[truth] = [0.15, 0.39, 0.66, 0.55]
        note = f"참 신호 {truth.sum():,}픽셀"
    else:
        over[mask & truth] = [0.15, 0.39, 0.66, 0.95]
        over[mask & ~truth] = [0.76, 0.25, 0.05, 0.95]
        note = f"참 양성 {(mask & truth).sum()}, 거짓 양성 {(mask & ~truth).sum()}"
    ax.imshow(over, origin="lower")
    ax.set_title(title, fontsize=9)
    ax.text(0.5, -0.04, note, transform=ax.transAxes, ha="center", va="top", fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color(C["gray"])


show(fig.add_subplot(gs[0, 0]), None, "(가) 참 신호의 위치")
show(fig.add_subplot(gs[0, 1]), masks["unc"], "(나) 비보정 p < 0.001")
show(fig.add_subplot(gs[1, 0]), masks["bonf"], "(라) 본페로니 FWE 5 %")
show(fig.add_subplot(gs[1, 1]), masks["perm"], "(마) 순열 최대 t, FWE 5 %")
show(fig.add_subplot(gs[1, 2]), masks["fdr"], "(바) BH FDR q = 0.05")

a = fig.add_subplot(gs[0, 2])
a.plot(rank, ps, color=C["blue"], lw=1.6, label="정렬한 p값")
a.plot(rank, 0.05 * rank / m, color=C["red"], lw=1.2, ls="--", label="BH 선 $q\\,k/m$")
a.axhline(0.05 / m, color=C["gray"], lw=1.0, ls=":", label="본페로니 $0.05/m$")
k = ok.max() + 1 if ok.size else 0
a.scatter([k], [ps[k - 1]], color=C["red"], s=20, zorder=3)
a.text(k * 1.25, ps[k - 1] * 0.9, f"$k$ = {k}", fontsize=8, color=C["red"], va="top")
a.set_xscale("log")
a.set_yscale("log")
a.set_xlim(1, 3000)
a.set_ylim(1e-9, 1)
a.set_xlabel("순위 $k$", fontsize=8.5)
a.set_ylabel("p값", fontsize=8.5)
a.yaxis.set_label_coords(-0.3, 0.5)
a.tick_params(labelsize=7.5)
a.set_title("(다) 벤야미니-호흐베르크", fontsize=9)
a.legend(fontsize=7, loc="lower right")

save(fig, __file__)
