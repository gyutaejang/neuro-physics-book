from figstyle import plt, np, save, C

# 복셀마다 SRTM과 로건 도표를 적합한 파라메트릭 BP_ND 지도. 복셀 잡음이 로건 지도를 낮게 끌어내린다.
dt = 0.01
t = np.arange(0, 90 + dt, dt)
A1, A2, A3, l1, l2, l3 = 851.1, 21.88, 20.81, 4.134, 0.1191, 0.01043
Cp = np.maximum((A1 * t - A2 - A3) * np.exp(-l1 * t) + A2 * np.exp(-l2 * t) + A3 * np.exp(-l3 * t), 0)


def tcm(K1, k2, k3, k4):
    a, b = np.zeros_like(t), np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (K1 * Cp[i - 1] - (k2 + k3) * a[i - 1] + k4 * b[i - 1])
        b[i] = b[i - 1] + dt * (k3 * a[i - 1] - k4 * b[i - 1])
    return a + b


CT, CR = tcm(0.1, 0.4, 0.24, 0.08), tcm(0.1, 0.4, 0.0, 0.0)
CX = tcm(0.1, 0.4, 0.04, 0.08)   # 피질 비슷한 낮은 결합 (BP_ND = 0.5)
dur = np.array([0.5] * 6 + [1] * 3 + [3] * 3 + [5] * 15)
ends = np.cumsum(dur)
starts, mid = ends - dur, ends - dur / 2
frame = lambda c: np.array([c[(t >= s) & (t < e)].mean() for s, e in zip(starts, ends)])
ct, cr, cx = frame(CT), frame(CR), frame(CX)

# 기저 함수: C_R ⊗ exp(-θt), θ = k2a 후보
thetas = np.geomspace(0.01, 1.0, 120)
basis = np.array([frame(np.convolve(CR, np.exp(-th * t) * dt)[: len(t)]) for th in thetas])
lam = np.log(2) / 20.4                                 # ¹¹C 붕괴 상수 (1/분)
var0 = ct * np.exp(lam * mid) / dur                    # 프레임 분산 ∝ 계수 / 길이
W = 1 / var0


def srtm(Y):
    """Y: (n, 프레임). 가중 최소제곱으로 θ마다 선형 적합하고 잔차가 가장 작은 θ를 고른다."""
    sw = np.sqrt(W)
    best, bp, fit = np.full(len(Y), np.inf), np.zeros(len(Y)), np.zeros_like(Y)
    for th, B in zip(thetas, basis):
        X = np.c_[cr, B]
        beta = np.linalg.lstsq(X * sw[:, None], (Y * sw).T, rcond=None)[0]
        rss = (((Y * sw).T - (X * sw[:, None]) @ beta) ** 2).sum(0)
        m = rss < best
        best[m] = rss[m]
        bp[m] = ((beta[1] + beta[0] * th) / th - 1)[m]
        fit[m] = (X @ beta).T[m]
    return bp, fit


def logan(Y, tstar=30, k2p=0.4):
    ict, icr = np.cumsum(Y * dur, 1), np.cumsum(cr * dur)
    x, y = ((icr + cr / k2p) / Y)[:, mid > tstar], (ict / Y)[:, mid > tstar]
    xm, ym = x.mean(1, keepdims=True), y.mean(1, keepdims=True)
    return ((x - xm) * (y - ym)).sum(1) / ((x - xm) ** 2).sum(1) - 1



# 2차원 팬텀 (2 mm 복셀 60 × 60): 선조체 두 개(BP 3), 피질 띠(BP 0.5), 나머지는 BP 0
n = 60
yy, xx = np.mgrid[0:n, 0:n] * 2.0 - 59
r = np.hypot(xx * 1.15, yy)
lab = np.zeros((n, n), int)
lab[(r > 42) & (r < 50)] = 2
lab[r >= 50] = -1                                   # 뇌 밖
for cx0 in (-13, 13):
    lab[((xx - cx0) / 6) ** 2 + (yy / 11) ** 2 <= 1] = 1
true = np.choose(lab + 1, [np.nan, 0.0, 3.0, 0.5])
tacs = {0: cr, 1: ct, 2: cx}
inside = lab >= 0
Yt = np.array([tacs[k] for k in lab[inside]])
var = Yt * np.exp(lam * mid) / dur
alpha = 0.25 * ct[-1] / np.sqrt(ct[-1] * np.exp(lam * mid[-1]) / dur[-1])   # 선조체 마지막 프레임 변동계수 25%
rng = np.random.default_rng(7)
Y = np.maximum(Yt + rng.standard_normal(Yt.shape) * alpha * np.sqrt(var), 0.05)
maps = {}
for name, fn in [("logan", logan), ("srtm", lambda v: srtm(v)[0])]:
    m = np.full((n, n), np.nan)
    m[inside] = fn(Y)
    maps[name] = m
roi_tac = Y[lab[inside] == 1].mean(0)[None]
roi = {"logan": logan(roi_tac)[0], "srtm": srtm(roi_tac)[0][0]}
vox = {k: np.nanmean(maps[k][lab == 1]) for k in maps}
cvox = {k: np.nanmean(maps[k][lab == 2]) for k in maps}
print("ROI-first", roi, "voxel-first striatum", vox, "cortex", cvox)

fig = plt.figure(figsize=(7.5, 2.75))
gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 0.07], wspace=0.06, left=0.0, right=0.66)
gr = fig.add_gridspec(1, 1, left=0.79, right=1.0, bottom=0.12, top=0.88)
cm = plt.get_cmap("magma").copy()
cm.set_bad("white")
for i, (img, ttl) in enumerate([(true, "(가) 참값"), (maps["logan"], "(나) 복셀별 로건"),
                                (maps["srtm"], "(다) 복셀별 SRTM")]):
    a = fig.add_subplot(gs[0, i])
    im = a.imshow(img, cmap=cm, vmin=0, vmax=4, origin="lower")
    a.set_xticks([])
    a.set_yticks([])
    for sp in a.spines.values():
        sp.set_visible(False)
    a.set_title(ttl, fontsize=9.5)
cax = fig.add_subplot(gs[0, 3])
cb = fig.colorbar(im, cax=cax)
cax.set_title("$BP_{ND}$", fontsize=8.5)
cb.ax.tick_params(labelsize=7.5)
cax.set_box_aspect(12)
a = fig.add_subplot(gr[0, 0])
for j, (k, lab) in enumerate([("logan", "로건"), ("srtm", "SRTM")]):
    a.plot(j - 0.12, vox[k], "o", color=C["red"], ms=7, label="복셀 지도의 ROI 평균" if j == 0 else None)
    a.plot(j + 0.12, roi[k], "s", color=C["blue"], ms=7, label="ROI 평균 TAC를 적합" if j == 0 else None)
    a.text(j - 0.2, vox[k], f"{vox[k]:.2f}", ha="right", va="center", fontsize=7.6, color=C["red"])
    a.text(j + 0.2, roi[k], f"{roi[k]:.2f}", ha="left", va="center", fontsize=7.6, color=C["blue"])
a.axhline(3, color=C["gray"], ls="--", lw=0.8)
a.set_xticks([0, 1])
a.set_xticklabels(["로건", "SRTM"])
a.set_xlim(-0.7, 1.7)
a.set_ylim(2.6, 3.2)
a.set_ylabel("선조체 $BP_{ND}$", fontsize=9)
a.legend(fontsize=7, loc="lower right", handletextpad=0.3)
a.set_title("(라) 선조체 평균", fontsize=9.5)
save(fig, __file__)
