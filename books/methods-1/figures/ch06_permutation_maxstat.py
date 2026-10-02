from scipy import ndimage, stats

from figstyle import plt, np, save, C

# 피험자 20명의 합성 대비 지도(96×96, FWHM 6픽셀 잡음 + 참 신호 세 덩어리), 단일 표본 t 검정.
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
X = noise + signal


def tmap(Y):
    return Y.mean(0) / (Y.std(0, ddof=1) / np.sqrt(N))


T = tmap(X)
maxT = np.empty(NPERM)
one = None
for i in range(NPERM):
    flip = rng.choice([-1.0, 1.0], N)[:, None, None]
    Tp = tmap(X * flip)
    maxT[i] = Tp.max()
    if i == 0:
        one = Tp.ravel()
t_perm = np.quantile(maxT, 0.95)
t_bonf = stats.t.isf(0.05 / L ** 2, N - 1)
t_unc = stats.t.isf(0.001, N - 1)

fig, ax = plt.subplots(figsize=(6.4, 3.0))
bins = np.linspace(-6, 11, 171)
ax.hist(one, bins=bins, density=True, color=C["gray"], alpha=0.45,
        label=f"순열 1회의 모든 복셀 t ({L * L:,}개)")
ax.hist(maxT, bins=bins, density=True, color=C["blue"], alpha=0.75,
        label=f"순열마다의 최대 t ({NPERM:,}회)")
ymax = ax.get_ylim()[1]
BB = dict(facecolor="white", edgecolor="none", pad=1.0)
ax.set_ylim(0, ymax * 1.5)
for x, col in [(t_unc, C["gray"]), (t_perm, C["blue"]), (t_bonf, C["red"])]:
    ax.axvline(x, color=col, lw=1.2, ls="--")
ax.text(t_unc - 0.12, ymax * 1.45, f"비보정 p<0.001\nt = {t_unc:.2f}", ha="right", va="top", fontsize=8, color=C["ink"], bbox=BB)
ax.text(t_perm - 0.12, ymax * 1.12, f"최대 t의 95 %\nt = {t_perm:.2f}", ha="right", va="top", fontsize=8, color=C["blue"], bbox=BB)
ax.text(t_bonf + 0.12, ymax * 1.12, f"본페로니\nt = {t_bonf:.2f}", ha="left", va="top", fontsize=8, color=C["red"], bbox=BB)
ax.text(T.max() - 0.3, ymax * 0.32, f"실제 지도의\n최대 t = {T.max():.1f}", ha="left", va="bottom", fontsize=8, color=C["ink"], bbox=BB)
ax.annotate("", xy=(T.max(), 0), xytext=(T.max(), ymax * 0.3),
            arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=0.8, mutation_scale=8))
ax.set_xlim(-6, 11)
ax.set_xlabel("t 값 (자유도 19)")
ax.set_ylabel("확률 밀도")
ax.set_yticks([])
ax.legend(fontsize=8, loc="upper left")
save(fig, __file__)
