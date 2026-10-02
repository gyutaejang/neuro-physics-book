from scipy import ndimage

from figstyle import plt, np, save, C
from ch03_bias_field import phantom, t1_image

# T1 강조(고정)와 T2 강조(움직이는 영상)의 회전 정합. 대비가 뒤집혀 있어도 상호 정보량은 맞는 각도에서 가장 크다.
frac = phantom()
t1 = t1_image(frac, seed=1)
MU2 = {"wm": 0.30, "gm": 0.48, "csf": 0.95, "skull": 0.05, "scalp": 0.55}
t2 = sum(frac[k] * MU2[k] for k in MU2) + 0.03 * np.random.default_rng(2).standard_normal(t1.shape)
roi = (slice(20, 172), slice(20, 172))


def joint(a, b, nb=40):
    h, _, _ = np.histogram2d(a.ravel(), b.ravel(), bins=nb, range=[[-0.05, 1.05], [-0.05, 1.05]])
    return h / h.sum()


def mi(a, b):
    p = joint(a, b)
    px, py = p.sum(1, keepdims=True), p.sum(0, keepdims=True)
    nz = p > 0
    return float((p[nz] * np.log2(p[nz] / (px @ py)[nz])).sum())


angles = np.linspace(-20, 20, 41)
mis, ssd, cc = [], [], []
for a in angles:
    r = ndimage.rotate(t2, a, reshape=False, order=1)
    A, B = t1[roi], r[roi]
    mis.append(mi(A, B))
    ssd.append(np.mean((A - B) ** 2))
    cc.append(np.corrcoef(A.ravel(), B.ravel())[0, 1])
mis, ssd, cc = map(np.array, (mis, ssd, cc))

if __name__ == "__main__":
    i0 = np.argmin(np.abs(angles))
    i8 = np.argmin(np.abs(angles - 8))
    print("MI 0°=%.3f 8°=%.3f 20°=%.3f bits" % (mis[i0], mis[i8], mis[-1]))
    print("SSD 최소 각도", angles[ssd.argmin()], "SSD 0°=%.4f 20°=%.4f" % (ssd[i0], ssd[-1]))
    print("상관 0°=%.3f 8°=%.3f" % (cc[i0], cc[i8]))

    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.7), gridspec_kw=dict(width_ratios=[1, 1, 1.3], wspace=0.42))
    for ax, a, ttl in [(axs[0], 0, "(가) 맞을 때 결합 히스토그램"), (axs[1], 8, "(나) 8° 어긋날 때")]:
        r = ndimage.rotate(t2, a, reshape=False, order=1)
        p = joint(t1[roi], r[roi], nb=60)
        ax.imshow(np.log10(p.T + 1e-5), origin="lower", extent=[-0.05, 1.05, -0.05, 1.05], cmap="Blues", vmin=-5, vmax=-1)
        ax.set_xlabel("T1 강조 밝기", fontsize=8.5)
        ax.set_ylabel("T2 강조 밝기", fontsize=8.5)
        ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
        ax.tick_params(labelsize=7.5)
        ax.set_title(ttl, fontsize=9.2)
        ax.text(0.97, 0.97, "MI = %.2f 비트" % mi(t1[roi], r[roi]), transform=ax.transAxes, ha="right", va="top", fontsize=7.5)
    for (xx, yy, t) in [(0.80, 0.30, "WM"), (0.50, 0.48, "GM"), (0.16, 0.95, "CSF")]:
        axs[0].text(xx + 0.05, yy + 0.08, t, fontsize=7.5, color=C["red"])
    ax = axs[2]
    ax.plot(angles, mis / mis.max(), color=C["blue"], lw=1.8, label="상호 정보량 (최댓값 = 1)")
    ax.plot(angles, ssd / ssd.max(), color=C["gray"], lw=1.4, ls="--", label="차이 제곱 평균 (최댓값 = 1)")
    ax.axvline(0, color=C["red"], lw=0.7, ls=":")
    ax.set_xlabel("회전 각도 (°)")
    ax.set_ylabel("상대값")
    ax.set_ylim(0, 1.32)
    ax.set_yticks([0, 0.5, 1])
    ax.legend(fontsize=7, loc="upper center")
    ax.set_title("(다) 각도에 따른 유사도와 비용", fontsize=9.2)
    save(fig, __file__)
