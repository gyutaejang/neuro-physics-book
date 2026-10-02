from scipy import ndimage

from figstyle import plt, np, save, C

# 순수 잡음장: 128×128 흰 잡음을 FWHM 8픽셀 가우스로 평활화하고 분산을 1로 맞춘다.
L, FWHM = 128, 8.0
sig = FWHM / np.sqrt(8 * np.log(2))
rng = np.random.default_rng(61)
delta = np.zeros((L, L))
delta[0, 0] = 1
k = ndimage.gaussian_filter(delta, sig, mode="wrap")
z = ndimage.gaussian_filter(rng.standard_normal((L, L)), sig, mode="wrap") / np.sqrt((k ** 2).sum())

fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.9))
panels = [(None, "(가) 신호 없는 z 지도"),
          (1.645, "(나) 비보정 p < 0.05 (z > 1.64)"),
          (3.09, "(다) 비보정 p < 0.001 (z > 3.09)")]
for ax, (thr, title) in zip(axs, panels):
    ax.imshow(z, cmap="Greys", vmin=-4, vmax=4, origin="lower")
    if thr is not None:
        mask = z > thr
        over = np.zeros((L, L, 4))
        over[mask] = [0.76, 0.25, 0.05, 0.95]
        ax.imshow(over, origin="lower")
        _, ncl = ndimage.label(mask)
        ax.text(0.5, -0.07, f"픽셀 {mask.mean() * 100:.2g} %, 덩어리 {ncl}개",
                transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color=C["red"])
    else:
        ax.text(0.5, -0.07, f"픽셀 {L * L:,}개, FWHM {FWHM:.0f}픽셀",
                transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color=C["ink"])
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(C["gray"])
fig.tight_layout(w_pad=0.6)
save(fig, __file__)
