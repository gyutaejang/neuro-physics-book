from scipy import ndimage, stats

from figstyle import plt, np, save, C

# 뇌 지도도 행동 점수도 순수 잡음이다. 참 상관은 어디서나 0이다.
L, N, FW, NSTUDY = 48, 20, 4.0, 1000
rng = np.random.default_rng(65)
s = FW / np.sqrt(8 * np.log(2))
p_sel = 0.001
tcrit = stats.t.isf(p_sel, N - 2)
r_crit = tcrit / np.sqrt(N - 2 + tcrit ** 2)


def maps(n):
    m = ndimage.gaussian_filter(rng.standard_normal((n, L, L)), (0, s, s), mode="wrap")
    return m / m.std()


def corr_map(Y, b):
    Yc = Y - Y.mean(0)
    bc = (b - b.mean()) / np.linalg.norm(b - b.mean())
    return np.tensordot(bc, Yc, axes=(0, 0)) / np.linalg.norm(Yc, axis=0)


circ, indep = [], []
example = None
for k in range(NSTUDY):
    Y, b = maps(N), rng.standard_normal(N)
    r = corr_map(Y, b)
    roi = r > r_crit
    if not roi.any():
        continue
    a = Y[:, roi].mean(1)
    rc = np.corrcoef(a, b)[0, 1]
    Y2, b2 = maps(N), rng.standard_normal(N)
    ri = np.corrcoef(Y2[:, roi].mean(1), b2)[0, 1]
    circ.append(rc)
    indep.append(ri)
    if example is None and roi.sum() > 8:
        example = (r, roi, a, b, rc, Y2[:, roi].mean(1), b2, ri)
circ, indep = np.array(circ), np.array(indep)
frac = len(circ) / NSTUDY

fig = plt.figure(figsize=(7.4, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[1.3, 1, 1.0], wspace=0.5)
r, roi, a, b, rc, a2, b2, ri = example
ax = fig.add_subplot(gs[0, 0])
im = ax.imshow(r, cmap="RdBu", vmin=-0.8, vmax=0.8, origin="lower")
ax.contour(roi, levels=[0.5], colors=[C["ink"]], linewidths=1.0, origin="lower")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("(가) 행동과의 상관 지도", fontsize=9)
ax.text(0.5, -0.04, f"검은 선: r > {r_crit:.2f} (p < {p_sel})", transform=ax.transAxes,
        ha="center", va="top", fontsize=8)
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, ticks=[-0.8, 0, 0.8])
cb.ax.tick_params(labelsize=7)

ax = fig.add_subplot(gs[0, 1])
ax.scatter(b, a, s=16, color=C["red"], label=f"같은 데이터: r = {rc:.2f}")
ax.scatter(b2, a2, s=16, facecolor="none", edgecolor=C["blue"], label=f"새 데이터: r = {ri:.2f}")
for xx, yy, col in [(b, a, C["red"]), (b2, a2, C["blue"])]:
    k1, k0 = np.polyfit(xx, yy, 1)
    g = np.array([-2.5, 2.5])
    ax.plot(g, k0 + k1 * g, color=col, lw=1)
ax.set_xlim(-2.8, 2.8)
ax.set_xlabel("행동 점수", fontsize=8.5)
ax.set_ylabel("ROI 평균 신호", fontsize=8.5)
ax.tick_params(labelsize=7.5)
ax.set_title("(나) 고른 ROI에서 다시 잰 상관", fontsize=9)
ax.legend(fontsize=7.5, loc="upper left", handletextpad=0.2)
lo, hi = ax.get_ylim()
ax.set_ylim(lo, hi + (hi - lo) * 0.35)

ax = fig.add_subplot(gs[0, 2])
bins = np.linspace(-1, 1, 41)
ax.hist(circ, bins=bins, color=C["red"], alpha=0.7, label=f"순환: 평균 {circ.mean():.2f}")
ax.hist(indep, bins=bins, color=C["blue"], alpha=0.6, label=f"독립: 평균 {indep.mean():.2f}")
ax.axvline(0, color=C["gray"], lw=0.8, ls=":")
ax.set_xlabel("ROI 상관 r", fontsize=8.5)
ax.set_yticks([])
ax.tick_params(labelsize=7.5)
ax.set_title(f"(다) 연구 {len(circ)}개의 분포", fontsize=9)
ax.legend(fontsize=7.5, loc="upper left")
lo, hi = ax.get_ylim()
ax.set_ylim(0, hi * 1.3)
save(fig, __file__)
