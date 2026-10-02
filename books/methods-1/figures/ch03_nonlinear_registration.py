from scipy import ndimage

from figstyle import plt, np, save, C
from ch03_bias_field import phantom, t1_image, brain_mask, N

# 주형(고정 영상)과 개인 뇌(머리가 작고 뇌실이 크다). 아핀(크기 맞춤) 뒤 데몬스 방식의 비선형 정합.
ftmp = phantom()
fsub = phantom(scale=0.92, vent=1.45)
S_TRUE = 0.92


def stripped(frac, seed):
    return t1_image(frac, noise=0.02, seed=seed) * brain_mask(frac)


F = stripped(ftmp, 3)
M0 = stripped(fsub, 4)
yy, xx = np.mgrid[0:N, 0:N].astype(float)
c0 = (N - 1) / 2

# 1) 아핀: 뇌 마스크 면적 비로 크기 배율을 추정해 중심 기준으로 늘린다.
s = np.sqrt(brain_mask(fsub).sum() / brain_mask(ftmp).sum())


def warp_scale(img, s):
    return ndimage.map_coordinates(img, [c0 + (yy - c0) * s, c0 + (xx - c0) * s], order=1)


M = warp_scale(M0, s)
Msub_gm = warp_scale(fsub["gm"], s)

# 2) 데몬스: 밝기 차이를 밝기 기울기 방향의 힘으로 바꾸고, 변위장을 가우스로 매끄럽게 한다.
ux = np.zeros((N, N)); uy = np.zeros((N, N))
gy, gx = np.gradient(ndimage.gaussian_filter(F, 0.7))
for it in range(400):
    Mw = ndimage.map_coordinates(M, [yy + uy, xx + ux], order=1)
    d = Mw - F
    den = gx ** 2 + gy ** 2 + d ** 2 + 1e-9
    ux -= d * gx / den
    uy -= d * gy / den
    ux = ndimage.gaussian_filter(ux, 2.0)
    uy = ndimage.gaussian_filter(uy, 2.0)
Mw = ndimage.map_coordinates(M, [yy + uy, xx + ux], order=1)
dxx = np.gradient(ux, axis=1); dxy = np.gradient(ux, axis=0)
dyx = np.gradient(uy, axis=1); dyy = np.gradient(uy, axis=0)
J_nl = (1 + dxx) * (1 + dyy) - dxy * dyx          # 비선형 부분의 야코비안 행렬식
J = J_nl * s ** 2                                  # 2차원이므로 아핀 배율의 제곱을 곱한다
mask = brain_mask(ftmp)

if __name__ == "__main__":
    print("추정 배율 %.3f (참 %.2f)" % (s, S_TRUE))
    r_aff = np.sqrt(np.mean((M - F)[mask] ** 2)); r_nl = np.sqrt(np.mean((Mw - F)[mask] ** 2))
    print("RMS 차이 아핀 %.3f 비선형 %.3f" % (r_aff, r_nl))
    print("J_nl 범위 %.2f–%.2f, 최소값>0? %s" % (J_nl[mask].min(), J_nl[mask].max(), J_nl.min() > 0))
    vent_t = (ftmp["csf"] > 0.5) & (np.abs(xx - c0) < 20) & (np.abs(yy - c0) < 40)
    print("뇌실 부근 평균 J_nl %.2f, 전체 J %.2f" % (J_nl[vent_t].mean(), J[vent_t].mean()))
    vt = (ftmp["csf"] * ((np.abs(xx - c0) < 20) & (np.abs(yy - c0) < 40))).sum()
    vs = (fsub["csf"] * ((np.abs(xx - c0) < 20 * 0.92) & (np.abs(yy - c0) < 40 * 0.92))).sum()
    print("뇌실 면적 주형 %.0f 개인 %.0f 비 %.2f" % (vt, vs, vs / vt))

    fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.45), gridspec_kw=dict(wspace=0.06))
    crop = (slice(18, 174), slice(26, 166))
    def show(ax, im, ttl, cont=True, **kw):
        h = ax.imshow(im[crop], **kw)
        if cont:
            ax.contour(F[crop], levels=[0.33, 0.65], colors=[C["red"]], linewidths=0.5)
        ax.set_title(ttl, fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        return h
    show(axs[0], M0, "(가) 개인 뇌", cmap="gray", vmin=0, vmax=1)
    show(axs[1], M, "(나) 아핀 정합 뒤", cmap="gray", vmin=0, vmax=1)
    show(axs[2], Mw, "(다) 비선형 정합 뒤", cmap="gray", vmin=0, vmax=1)
    h = show(axs[3], np.where(mask, np.log2(J_nl), np.nan), "(라) 비선형 부분의 J", cont=False,
             cmap="RdBu_r", vmin=-0.6, vmax=0.6)
    cax = axs[3].inset_axes([0.12, -0.07, 0.76, 0.04])
    cb = fig.colorbar(h, cax=cax, orientation="horizontal", ticks=np.log2([0.7, 1, 1.4]))
    cb.ax.set_xticklabels(["0.7", "1", "1.4"])
    cb.ax.tick_params(labelsize=7, length=2)
    save(fig, __file__)
