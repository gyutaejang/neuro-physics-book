from figstyle import plt, np, save, C
from scipy import ndimage

# 펼친 피질 조각 120 × 120 mm 위의 같은 효과를 세 가지 분할로 요약한다.
n = 120
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:n, 0:n]
effect = 1.0 * np.exp(-(((xx - 60) ** 2 + (yy - 60) ** 2) / (2 * 9.0 ** 2)))   # 참 효과(최대 1)
noise = ndimage.gaussian_filter(rng.normal(0, 1, (n, n)), 3) * 2.0
data = effect + noise


def grid_labels(off, w=40):
    return ((xx + w - off) // w) + 10 * ((yy + w - off) // w)


def voronoi_labels(k, seed):
    r = np.random.default_rng(seed)
    pts = r.uniform(0, n, (k, 2))
    d = (xx[..., None] - pts[:, 0]) ** 2 + (yy[..., None] - pts[:, 1]) ** 2
    return d.argmin(-1)


atlases = [("(가) 40 mm 격자 9칸", grid_labels(40)),
           ("(나) 같은 격자, 20 mm 옮김", grid_labels(60)),
           ("(다) 작은 영역 40개", voronoi_labels(40, 5))]


def region_mean(lab, val):
    ids = np.unique(lab)
    m = ndimage.mean(val, lab, ids)
    out = np.zeros_like(val)
    for i, v in zip(ids, m):
        out[lab == i] = v
    return out


fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.35), gridspec_kw=dict(wspace=0.08))
a = axs[0]
a.imshow(data, cmap="RdBu_r", vmin=-1.2, vmax=1.2)
a.contour(effect, levels=[0.5], colors=[C["ink"]], linewidths=0.8)
a.set_title("자료: 참 효과 + 잡음", fontsize=9.5)
best = []
for a, (title, lab) in zip(axs[1:], atlases):
    rm = region_mean(lab, data)
    a.imshow(rm, cmap="RdBu_r", vmin=-1.2, vmax=1.2)
    edge = (np.diff(lab, axis=0, prepend=lab[:1]) != 0) | (np.diff(lab, axis=1, prepend=lab[:, :1]) != 0)
    a.imshow(np.ma.masked_where(~edge, edge), cmap="Greys", vmin=0, vmax=1, interpolation="nearest")
    a.contour(effect, levels=[0.5], colors=[C["ink"]], linewidths=0.8, linestyles="--")
    a.set_title(title, fontsize=9.5)
    best.append(rm[59, 59])
    a.set_xlabel(f"중심 영역 평균 {rm[59, 59]:.2f}".replace("-", "−"), fontsize=8.5)
for a in axs:
    a.set_xticks([]); a.set_yticks([])
axs[0].set_xlabel("실선: 참 효과의 절반 높이", fontsize=8.5)
save(fig, __file__)
