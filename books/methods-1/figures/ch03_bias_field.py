from figstyle import plt, np, save, C

# 3장 공용 합성 팬텀: 192 × 192, 픽셀 1 mm. 4배 세밀한 격자에서 조직을 그린 뒤 평균해
# 복셀마다 조직 분율(부분 용적)을 얻는다. 다른 ch03 그림이 이 모듈을 import한다.
N = 192
SUB = 4
MU = {"wm": 0.80, "gm": 0.50, "csf": 0.15, "skull": 0.05, "scalp": 0.70}   # T1 강조 밝기
SIGMA = 0.03                                                                # 열잡음 표준편차


def _labels(n=N, sub=SUB, scale=1.0, vent=1.0, thick=3.0):
    from scipy import ndimage
    m = n * sub
    y, x = np.mgrid[0:m, 0:m]
    x = (x + 0.5) / sub - n / 2
    y = (y + 0.5) / sub - n / 2
    th = np.arctan2(y, x)
    rho = np.sqrt((x / (74 * scale)) ** 2 + (y / (88 * scale)) ** 2)
    # 고랑: 좁고 깊은 홈 28개(깊이가 조금씩 다르다)와 앞뒤 대뇌 반구 사이 틈
    ph = 28 * th + 0.5 * np.sin(3 * th)
    depth = 0.17 + 0.05 * np.sin(5 * th + 1.0)
    groove = np.cos(ph / 2) ** 40
    fiss = np.exp(-(x / (1.5 * scale)) ** 2) * (np.abs(y) > 38 * scale)
    outer = rho < 1.0
    brain = (rho < 1.0 - depth * groove) & (fiss < 0.5)
    d_out = ndimage.distance_transform_edt(brain) / sub         # 피질 겉면에서 잰 깊이(mm)
    lab = np.zeros((m, m), dtype=np.int8)            # 0 배경
    lab[rho < 1.14] = 5                              # 두피
    lab[rho < 1.07] = 4                              # 두개골
    lab[rho < 1.025] = 3                             # 뇌척수액
    lab[brain] = 2                                   # 회백질
    lab[brain & (d_out > thick * scale)] = 1         # 백질: 겉면에서 두께보다 깊은 곳

    def ell(a, b, x0, y0, ang=0.0):
        c, s = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
        xr, yr = (x - x0) * c + (y - y0) * s, -(x - x0) * s + (y - y0) * c
        return (xr / a) ** 2 + (yr / b) ** 2 <= 1

    for sgn in (-1, 1):
        lab[ell(10 * scale, 14 * scale, sgn * 14 * scale, 10 * scale)] = 2      # 시상
        lab[ell(6 * scale, 17 * scale, sgn * 27 * scale, -8 * scale, -sgn * 8)] = 2   # 조가비핵
        lab[ell(5 * vent * scale, 19 * vent * scale, sgn * 7 * scale, -12 * scale, -sgn * 12)] = 3  # 뇌실
    return lab


def phantom(scale=1.0, vent=1.0):
    """복셀별 조직 분율 dict(wm, gm, csf, skull, scalp)를 돌려준다."""
    lab = _labels(scale=scale, vent=vent)
    out = {}
    for k, v in zip(["wm", "gm", "csf", "skull", "scalp"], [1, 2, 3, 4, 5]):
        out[k] = (lab == v).reshape(N, SUB, N, SUB).mean(axis=(1, 3))
    return out


def t1_image(frac, noise=SIGMA, seed=0):
    img = sum(frac[k] * MU[k] for k in MU)
    rng = np.random.default_rng(seed)
    return img + noise * rng.standard_normal(img.shape)


def brain_mask(frac):
    return (frac["wm"] + frac["gm"] + frac["csf"]) > 0.5


def coords():
    y, x = np.mgrid[0:N, 0:N]
    return (x - N / 2) / (N / 2), (y - N / 2) / (N / 2)


def bias_field():
    """수신 코일 민감도를 흉내 낸 매끄러운 곱셈 장(뇌 안에서 약 0.8–1.2)."""
    u, v = coords()
    return np.exp(0.17 * v - 0.08 * u + 0.09 * (u ** 2 + v ** 2) - 0.09)


def poly_basis(u, v, deg=3):
    return np.stack([u ** i * v ** j for i in range(deg + 1) for j in range(deg + 1 - i)], axis=-1)


def correct_bias(img, mask, n_iter=8, deg=3):
    """N4의 생각을 줄인 판: 조직 평균으로 나눈 로그 잔차를 매끄러운 다항식으로 맞추기를 되풀이."""
    u, v = coords()
    A = poly_basis(u[mask], v[mask], deg)
    logb = np.zeros_like(img)
    for _ in range(n_iter):
        c = img / np.exp(logb)
        vals = c[mask]
        cent = np.quantile(vals, [0.1, 0.5, 0.9])
        for _k in range(10):                                   # 1차원 k-평균으로 조직 평균
            cls = np.argmin(np.abs(vals[:, None] - cent[None]), axis=1)
            cent = np.array([vals[cls == j].mean() for j in range(3)])
        target = cent[cls]
        ok = target > 0.3                                       # 어두운 뇌척수액은 잡음이 커서 뺀다
        r = np.log(np.clip(img[mask][ok], 1e-3, None)) - np.log(target[ok])
        coef, *_ = np.linalg.lstsq(A[ok], r, rcond=None)
        full = poly_basis(u, v, deg) @ coef
        logb = full - full[mask].mean()
    return np.exp(logb)


if __name__ == "__main__":
    frac = phantom()
    true = t1_image(frac)
    mask = brain_mask(frac)
    b = bias_field()
    raw = true * b
    best = correct_bias(raw, mask)
    corr = raw / best
    wm = frac["wm"] > 0.99
    gm = frac["gm"] > 0.99
    for name, im in [("참", true), ("편향", raw), ("보정", corr)]:
        print(name, "WM CV %.3f" % (im[wm].std() / im[wm].mean()),
              "WM 범위 %.2f–%.2f" % tuple(np.percentile(im[wm], [2, 98])),
              "GM 범위 %.2f–%.2f" % tuple(np.percentile(im[gm], [2, 98])))
    print("편향장 뇌 안 범위 %.2f–%.2f" % (b[mask].min(), b[mask].max()))
    print("추정/참 비 범위 %.3f–%.3f" % tuple(np.percentile((best / b)[mask] / np.mean((best / b)[mask]), [1, 99])))

    fig = plt.figure(figsize=(7.4, 3.0))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.35], wspace=0.12)
    crop = (slice(8, 184), slice(16, 176))
    titles = ["(가) 받은 영상", "(나) 추정한 편향장", "(다) 보정한 영상"]
    for i, (im, kw) in enumerate([(raw, dict(cmap="gray", vmin=0, vmax=1)),
                                  (np.where(mask, best, np.nan), dict(cmap="RdBu_r", vmin=0.75, vmax=1.25)),
                                  (corr * mask, dict(cmap="gray", vmin=0, vmax=1))]):
        ax = fig.add_subplot(gs[i])
        h = ax.imshow(im[crop], **kw)
        ax.set_title(titles[i], fontsize=9.5)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        if i == 1:
            cax = ax.inset_axes([0.15, -0.09, 0.7, 0.045])
            cb = fig.colorbar(h, cax=cax, orientation="horizontal", ticks=[0.8, 1.0, 1.2])
            cb.ax.tick_params(labelsize=7, length=2)
    ax = fig.add_subplot(gs[3])
    bins = np.linspace(0.05, 1.05, 101)
    ax.hist(raw[mask], bins=bins, histtype="step", color=C["gray"], lw=1.2, label="보정 전")
    ax.hist(corr[mask], bins=bins, histtype="step", color=C["blue"], lw=1.4, label="보정 후")
    ax.set_xlabel("밝기", fontsize=8.5)
    ax.set_box_aspect(1.05)
    ax.set_yticks([])
    ax.tick_params(labelsize=7.5)
    ax.set_title("(라) 뇌 안 밝기 히스토그램", fontsize=9.5)
    for xx, t in [(0.15, "CSF"), (0.5, "GM"), (0.8, "WM")]:
        ax.text(xx, ax.get_ylim()[1] * 0.98, t, ha="center", va="top", fontsize=7.5, color=C["ink"])
    ax.legend(fontsize=7.5, loc="upper left", bbox_to_anchor=(0.06, 0.86))
    save(fig, __file__)
