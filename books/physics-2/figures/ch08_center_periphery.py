from figstyle import plt, np, save, C
from ch08_phantom_kspace import phantom, N

# k-공간 중심만, 또는 가장자리만 남기고 역푸리에 변환한다.
img = phantom()
K = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(img)))
ky, kx = np.mgrid[-N // 2:N // 2, -N // 2:N // 2]
half = 16                                    # 중심 32 × 32 (전체의 1/64)
center = (np.abs(kx) < half) & (np.abs(ky) < half)


def recon(mask):
    return np.real(np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(K * mask))))


r_c = recon(center)
r_p = np.abs(recon(~center))
logK = np.log10(np.abs(K) + 1e-3)
vmin, vmax = logK.max() - 5, logK.max()

fig, axs = plt.subplots(2, 3, figsize=(7.2, 4.8), gridspec_kw=dict(hspace=0.12, wspace=0.12))
panels = [
    (np.ones_like(center, dtype=bool), img, "(가) 전체 256 × 256", (0, 1)),
    (center, r_c, "(나) 중심 32 × 32만", (0, 1)),
    (~center, r_p, "(다) 중심을 뺀 가장자리만", (0, np.percentile(r_p, 99.7))),
]
for j, (mask, rec, title, (lo, hi)) in enumerate(panels):
    ax = axs[0, j]
    ax.imshow(np.where(mask, logK, np.nan), cmap="magma", vmin=vmin, vmax=vmax)
    ax.set_facecolor("#d9d9d9")
    ax.set_title(title, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax2 = axs[1, j]
    ax2.imshow(rec, cmap="gray", vmin=lo, vmax=hi)
    ax2.set_xticks([]); ax2.set_yticks([])
axs[0, 0].set_ylabel("남긴 k-공간", fontsize=9.5)
axs[1, 0].set_ylabel("역푸리에 변환", fontsize=9.5)
axs[1, 1].set_xlabel("밝기와 대비는 남고\n경계가 흐려진다", fontsize=9)
axs[1, 2].set_xlabel("경계만 남는다\n(밝기 범위를 늘려 표시)", fontsize=9)
axs[1, 0].set_xlabel("원래 영상", fontsize=9)
save(fig, __file__)
