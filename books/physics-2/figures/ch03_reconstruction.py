from figstyle import plt, np, save, C

# 2차원 PET 모형: 사이노그램, 단순 역투영, 필터 역투영, 반복 재구성(MLEM)
N = 96
yy, xx = (np.mgrid[0:N, 0:N] - (N - 1) / 2) / (N / 2)


def ell(cx, cy, a, b):
    return ((xx - cx) / a) ** 2 + ((yy - cy) / b) ** 2 <= 1


img = np.zeros((N, N))
img[ell(0, 0, 0.72, 0.88)] = 1.0          # 백질 수준
img[ell(0, 0, 0.72, 0.88) & ~ell(0, 0, 0.62, 0.78)] = 3.0  # 피질 띠
img[ell(-0.22, 0.05, 0.1, 0.14)] = 4.0     # 선조체 (뜨거운 곳)
img[ell(0.22, 0.05, 0.1, 0.14)] = 4.0
img[ell(0.0, -0.45, 0.12, 0.08)] = 0.0    # 차가운 곳 (병변)

angles = np.linspace(0, np.pi, 120, endpoint=False)


def rotate(a, th):
    """a를 각 th만큼 돌린 영상 (쌍선형 보간)."""
    c, s = np.cos(th), np.sin(th)
    cx = (N - 1) / 2
    X, Y = np.meshgrid(np.arange(N) - cx, np.arange(N) - cx)
    xs = c * X + s * Y + cx
    ys = -s * X + c * Y + cx
    x0, y0 = np.floor(xs).astype(int), np.floor(ys).astype(int)
    fx, fy = xs - x0, ys - y0
    out = np.zeros_like(a)
    for dx_, dy_, w in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)),
                        (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        xi, yi = x0 + dx_, y0 + dy_
        ok = (xi >= 0) & (xi < N) & (yi >= 0) & (yi < N)
        out[ok] += w[ok] * a[yi[ok], xi[ok]]
    return out


def project(a):
    return np.array([rotate(a, th).sum(axis=0) for th in angles])


def backproject(s):
    out = np.zeros((N, N))
    for th, p in zip(angles, s):
        out += rotate(np.tile(p, (N, 1)), -th)
    return out


rng = np.random.default_rng(1)
sino_true = project(img)
scale = 2.0
sino = rng.poisson(sino_true * scale) / scale

bp = backproject(sino)
# 램프 필터 (주파수 공간에서 |f|를 곱한다), 약한 해밍 창
f = np.fft.fftfreq(N)
ramp = np.abs(f) * (0.54 + 0.46 * np.cos(2 * np.pi * f))
fsino = np.real(np.fft.ifft(np.fft.fft(sino, axis=1) * ramp, axis=1))
fbp = backproject(fsino)

# MLEM
x = np.ones((N, N))
sens = backproject(np.ones_like(sino))
mask = sens > 0
for it in range(30):
    proj = project(x)
    ratio = np.where(proj > 1e-6, sino / np.maximum(proj, 1e-6), 0)
    x = np.where(mask, x * backproject(ratio) / np.maximum(sens, 1e-6), 0)

fig, axs = plt.subplots(1, 5, figsize=(7.4, 1.95), gridspec_kw=dict(width_ratios=[1, 1.25, 1, 1, 1]))
titles = ["(가) 참 분포", "(나) 사이노그램", "(다) 단순 역투영", "(라) 필터 역투영", "(마) 반복 재구성"]
ims = [img, sino, bp, fbp, x]
for a, im, t in zip(axs, ims, titles):
    if t.startswith("(나)"):
        a.imshow(im, cmap="gray", aspect="auto", extent=[-1, 1, 180, 0])
        a.set_xlabel("응답선 위치", fontsize=7.5)
        a.set_ylabel("각도 (°)", fontsize=7.5, labelpad=1)
        a.set_yticks([0, 90, 180])
        a.set_xticks([])
        a.tick_params(labelsize=7)
    else:
        lo = np.percentile(im, 1) if t.startswith("(라)") else 0
        a.imshow(im, cmap="gray", vmin=lo, vmax=np.percentile(im, 99.7))
        a.set_xticks([])
        a.set_yticks([])
        for sp in a.spines.values():
            sp.set_visible(False)
    a.set_title(t, fontsize=8.5)
fig.tight_layout(w_pad=0.6)
save(fig, __file__)
