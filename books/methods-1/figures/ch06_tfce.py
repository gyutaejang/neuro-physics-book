from matplotlib.colors import PowerNorm
from scipy import ndimage

from figstyle import plt, np, save, C

E, H, DH = 0.5, 2.0, 0.05


def tfce(img):
    """모든 높이 h에서 '이 점이 속한 덩어리 크기^E × h^H'를 더한다."""
    out = np.zeros_like(img)
    for h in np.arange(DH, img.max() + DH, DH):
        lab, n = ndimage.label(img >= h)
        if n == 0:
            break
        size = np.bincount(lab.ravel()).astype(float)
        size[0] = 0
        out += size[lab] ** E * h ** H * DH
    return out


# 1차원 단면: 좁고 높은 봉우리와 넓고 낮은 언덕
x = np.arange(0, 120, 0.25)
prof = 4.0 * np.exp(-(x - 30) ** 2 / (2 * 2.0 ** 2)) + 2.2 * np.exp(-(x - 80) ** 2 / (2 * 10 ** 2))
tf1 = tfce(prof) * 0.25 ** E  # 길이 단위를 픽셀(0.25)에서 1로 맞춘다

# 2차원: ch06_cluster_forming.py와 같은 z 지도
L, FW = 128, 6.0
rng = np.random.default_rng(64)
s = FW / np.sqrt(8 * np.log(2))
d = np.zeros((L, L))
d[0, 0] = 1
norm = np.sqrt((ndimage.gaussian_filter(d, s, mode="wrap") ** 2).sum())
yy, xx = np.mgrid[0:L, 0:L]
blob = lambda cy, cx, w, a: a * np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * w ** 2))
signal = blob(84, 34, 5, 3.8) + blob(84, 48, 5, 3.8) + blob(36, 86, 12, 2.0)
z = ndimage.gaussian_filter(rng.standard_normal((L, L)), s, mode="wrap") / norm + signal
tf2 = tfce(np.clip(z, 0, None))

fig = plt.figure(figsize=(7.3, 5.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1], hspace=0.35, wspace=0.08)
a1 = fig.add_subplot(gs[0, 0])
a1.fill_between(x, 0, prof, color=C["light"])
a1.plot(x, prof, color=C["blue"], lw=1.6)
for h in (0.5, 1.5, 2.5, 3.5):
    on = prof >= h
    edges = np.flatnonzero(np.diff(np.r_[0, on.astype(int), 0]))
    for i0, i1 in zip(edges[::2], edges[1::2]):
        a1.plot([x[i0], x[i1 - 1]], [h, h], color=C["red"], lw=1.4)
    a1.text(121, h, f"h = {h}", fontsize=7.5, color=C["red"], va="center")
a1.set_xlim(0, 130)
a1.set_ylim(0, 4.6)
a1.set_ylabel("통계량 z")
a1.set_title("(가) 높이 h마다 문턱을 그어 덩어리 폭 e(h)를 잰다", fontsize=9)
a1.set_xticklabels([])

a2 = fig.add_subplot(gs[1, 0])
a2.plot(x, tf1, color=C["purple"], lw=1.8)
for xc in (30, 80):
    i = np.argmin(abs(x - xc))
    a2.text(xc, tf1[i] + 0.04 * tf1.max(), f"{tf1[i]:.0f}", ha="center", va="bottom", fontsize=8, color=C["purple"])
a2.set_xlim(0, 130)
a2.set_ylim(0, tf1.max() * 1.25)
a2.set_xlabel("위치 (픽셀)")
a2.set_ylabel("TFCE 점수")
a2.set_title("(나) TFCE = Σ e(h)$^{0.5}$ h$^{2}$ Δh", fontsize=9)

for j, (img, title, cmap, vmax) in enumerate([(z, "(다) z 지도", "Greys", 5),
                                              (tf2, "(라) TFCE 지도 (제곱근 눈금)", "Purples", None)]):
    ax = fig.add_subplot(gs[j, 1])
    if j == 0:
        ax.imshow(img, cmap=cmap, vmin=-5, vmax=5, origin="lower")
    else:
        ax.imshow(img, cmap=cmap, norm=PowerNorm(0.5, vmin=0, vmax=img.max()), origin="lower")
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color(C["gray"])
save(fig, __file__)
