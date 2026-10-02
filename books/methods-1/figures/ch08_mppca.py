from figstyle import plt, np, save, C

# MP-PCA 잡음 제거의 원리를 합성 확산 데이터로 보인다.
# 48 x 48 단면, b = 0 영상 6개 + b = 1000 s/mm² 60방향, 라이스 잡음(b = 0 조직 SNR 15).
rng = np.random.default_rng(8)
n = 48
nb0, ndir, b = 6, 60, 1.0  # b를 10³ s/mm² 단위로, D를 10⁻³ mm²/s 단위로 쓴다


def fib_hemisphere(k):
    i = np.arange(k) + 0.5
    z = i / k  # 위 반구
    phi = np.pi * (1 + 5 ** 0.5) * i
    r = np.sqrt(1 - z ** 2)
    return np.stack([r * np.cos(phi), r * np.sin(phi), z], 1)


g = fib_hemisphere(ndir)
bvals = np.r_[np.zeros(nb0), np.full(ndir, b)]
bvecs = np.r_[np.zeros((nb0, 3)), g]

# 조직: 회백질(등방 0.8), 가로 백질 다발, 세로 백질 다발, 뇌실(물 3.0, T2가 길어 b0가 밝다)
yy, xx = np.mgrid[0:n, 0:n]
S0 = np.ones((n, n))
D = np.zeros((n, n, 3, 3))
D[...] = np.eye(3) * 0.8
wm_h = (yy >= 16) & (yy < 26)
wm_v = (xx >= 32) & (xx < 40)
for mask, u in ((wm_h, np.array([1.0, 0, 0])), (wm_v, np.array([0, 1.0, 0]))):
    T = 0.3 * np.eye(3) + 1.4 * np.outer(u, u)
    D[mask] = T
csf = (xx - 14) ** 2 + (yy - 36) ** 2 < 6 ** 2
D[csf] = np.eye(3) * 3.0
S0[csf] = 1.6
S0[wm_h | wm_v] = 0.85

adc = np.einsum("ki,xyij,kj->xyk", bvecs, D, bvecs)
clean = S0[..., None] * np.exp(-bvals * adc)
sigma = 1 / 15
noisy = np.abs(clean + sigma * rng.standard_normal(clean.shape)
               + 1j * sigma * rng.standard_normal(clean.shape))


def mp_denoise_patch(X):
    """X: (복셀 M, 볼륨 N). 마르첸코-파스투르 문턱으로 잡음 성분을 버린다."""
    M, N = X.shape
    mean = X.mean(0, keepdims=True)
    Y = X - mean
    U, s, Vt = np.linalg.svd(Y, full_matrices=False)
    m, nn = min(M - 1, N), max(M, N)  # 평균을 뺐으므로 계수가 하나 준다
    lam = s[:m] ** 2 / nn
    # 큰 고윳값부터 신호로 떼어 내며, 남은 것이 MP 분포의 폭과 맞는 첫 지점을 찾는다.
    for p in range(m):
        rest = lam[p:]
        gamma = (m - p) / nn
        sig2 = rest.mean()
        if (rest[0] - rest[-1]) < 4 * np.sqrt(gamma) * sig2:
            break
    keep = p
    Xd = (U[:, :keep] * s[:keep]) @ Vt[:keep] + mean
    return Xd, lam, keep, sig2


h = 2  # 5 x 5 창
den = noisy.copy()
sig_map = np.full((n, n), np.nan)
for i in range(n):
    for j in range(n):
        i0, i1 = max(i - h, 0), min(i + h + 1, n)
        j0, j1 = max(j - h, 0), min(j + h + 1, n)
        P = noisy[i0:i1, j0:j1].reshape(-1, noisy.shape[2])
        Pd, lam, keep, s2 = mp_denoise_patch(P)
        ci = (i - i0) * (j1 - j0) + (j - j0)
        den[i, j] = Pd[ci]
        sig_map[i, j] = np.sqrt(s2)

# 한 창의 고윳값 스펙트럼 (가로 다발과 회백질 경계)
P = noisy[26 - h:27 + h, 32 - h:33 + h].reshape(-1, noisy.shape[2])
_, lam_ex, keep_ex, s2_ex = mp_denoise_patch(P)


def fit_fa(S):
    Sl = np.log(np.clip(S, 1e-4, None)).reshape(-1, S.shape[-1])
    B = np.c_[np.ones(len(bvals)), -bvals[:, None] * np.c_[
        bvecs[:, 0] ** 2, bvecs[:, 1] ** 2, bvecs[:, 2] ** 2,
        2 * bvecs[:, 0] * bvecs[:, 1], 2 * bvecs[:, 0] * bvecs[:, 2], 2 * bvecs[:, 1] * bvecs[:, 2]]]
    coef = np.linalg.lstsq(B, Sl.T, rcond=None)[0].T
    Dxx, Dyy, Dzz, Dxy, Dxz, Dyz = coef[:, 1:].T
    T = np.stack([np.stack([Dxx, Dxy, Dxz], -1), np.stack([Dxy, Dyy, Dyz], -1),
                  np.stack([Dxz, Dyz, Dzz], -1)], -2)
    ev = np.linalg.eigvalsh(T)
    md = ev.mean(-1, keepdims=True)
    fa = np.sqrt(1.5 * ((ev - md) ** 2).sum(-1) / (ev ** 2).sum(-1))
    return fa.reshape(S.shape[:2])


fa_true, fa_noisy, fa_den = fit_fa(clean), fit_fa(noisy), fit_fa(den)
inner = np.zeros((n, n), bool)
inner[3:-3, 3:-3] = True
for name, m in (("백질", (wm_h | wm_v) & inner), ("회백질", ~(wm_h | wm_v | csf) & inner)):
    e1 = np.sqrt(np.mean((fa_noisy[m] - fa_true[m]) ** 2))
    e2 = np.sqrt(np.mean((fa_den[m] - fa_true[m]) ** 2))
    print(f"{name}: 참 FA {fa_true[m].mean():.2f}, 잡음 {fa_noisy[m].mean():.3f} (RMSE {e1:.3f}),"
          f" 제거 후 {fa_den[m].mean():.3f} (RMSE {e2:.3f})")
print("시그마 추정 중앙값", np.nanmedian(sig_map[inner & ~csf]), "참", sigma, "예시 창 신호 성분", keep_ex)
gm = ~(wm_h | wm_v | csf) & inner
print("b=1000 회백질 SNR", (clean[gm][:, nb0:].mean() / sigma))

# ---- 그림
k = nb0 + 7  # 보여 줄 확산 방향
fig = plt.figure(figsize=(7.4, 2.75))
ax0 = fig.add_axes([0.065, 0.2, 0.25, 0.66])
idx = np.arange(1, len(lam_ex) + 1)
ax0.semilogy(idx, lam_ex, "o", ms=3.2, color=C["blue"], label="실제 창")
lo = s2_ex * (1 - np.sqrt((len(lam_ex) - keep_ex) / P.shape[1])) ** 2
hi = s2_ex * (1 + np.sqrt((len(lam_ex) - keep_ex) / P.shape[1])) ** 2
ax0.axhspan(lo, hi, color=C["gray"], alpha=0.18, lw=0)
ax0.text(len(lam_ex) * 0.98, hi * 1.25, "MP 잡음 띠", ha="right", fontsize=8, color=C["gray"])
for q in range(keep_ex):
    ax0.semilogy(idx[q], lam_ex[q], "o", ms=4.2, color=C["red"])
ax0.text(keep_ex + 1.3, lam_ex[0] * 0.5, f"신호 성분 {keep_ex}개", fontsize=8, color=C["red"])
ax0.set_xlabel("주성분 순위")
ax0.set_ylabel("고윳값")
ax0.set_title("(가) 5×5 창의 고윳값", fontsize=9.5)
ax0.set_xticks([1, 10, 20])
ax0.set_ylim(lam_ex.min() * 0.4, lam_ex.max() * 3)

vmax = np.percentile(noisy[..., k], 99.5)
titles = ("(나) 잡음 있는 DWI", "(다) MP-PCA 뒤", "(라) 빼낸 것(잔차)")
imgs = (noisy[..., k], den[..., k], noisy[..., k] - den[..., k])
for i, (im, t) in enumerate(zip(imgs, titles)):
    ax = fig.add_axes([0.375 + i * 0.21, 0.12, 0.2, 0.74])
    if i < 2:
        ax.imshow(im, cmap="gray", vmin=0, vmax=vmax, origin="lower")
    else:
        ax.imshow(im, cmap="gray", vmin=-3 * sigma, vmax=3 * sigma, origin="lower")
    ax.set_title(t, fontsize=9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color(C["gray"])
fig.text(0.375 + 2 * 0.21 + 0.1, 0.04, "구조가 보이지 않아야 한다", ha="center", fontsize=8, color=C["gray"])
fig.text(0.375 + 0.1, 0.04, f"회백질 FA 오차 {np.sqrt(np.mean((fa_noisy[gm]-fa_true[gm])**2)):.2f}",
         ha="center", fontsize=8, color=C["gray"])
fig.text(0.375 + 0.21 + 0.1, 0.04, f"회백질 FA 오차 {np.sqrt(np.mean((fa_den[gm]-fa_true[gm])**2)):.2f}",
         ha="center", fontsize=8, color=C["gray"])
save(fig, __file__)
