import sys

from scipy.signal import butter, sosfiltfilt, hilbert

from figstyle import plt, np, save, C

# 소스 누설의 장난감 모형. 깊이 2.5 cm의 1차원 피질 위 0.25 cm 간격 소스점, 그 위 33개 센서.
# 리드필드는 수직 쌍극자의 두피 전위 꼴 d/(Δx² + d²)^1.5, 역해는 최소 노름(MNE).
# ROI는 폭 1 cm, 중심 0, 1, …, 5 cm. ROI마다 서로 독립인 베타 소스가 하나씩 있고,
# 4 cm ROI만 0 cm ROI와 포락선이 실제로 결합해 있다.
rng = np.random.default_rng(2)
xs = np.arange(-12, 12.01, 0.75)
xg = np.arange(-6, 9.01, 0.25)
dep = 2.5
L = dep / ((xs[:, None] - xg[None, :]) ** 2 + dep**2) ** 1.5
L /= np.abs(L).max()
lam2 = 0.05 * np.trace(L @ L.T) / len(xs)
K = L.T @ np.linalg.inv(L @ L.T + lam2 * np.eye(len(xs)))
R = K @ L
centers = np.arange(0, 6)
rois = [np.where(np.abs(xg - c) <= 0.5)[0] for c in centers]

fs, dur = 200, 300
n = fs * dur
fr = np.fft.rfftfreq(n, 1 / fs)
band = butter(4, [15, 25], btype="band", fs=fs, output="sos")


def lowz(m):
    X = np.fft.rfft(rng.normal(size=(m, n)), axis=1) * (fr < 0.2)
    x = np.fft.irfft(X, n, axis=1)
    return x / x.std(axis=1, keepdims=True)


slow = lowz(len(centers))
slow[4] = 0.8 * slow[0] + 0.6 * slow[4]          # 4 cm ROI만 0 cm ROI와 포락선 결합
car = sosfiltfilt(band, rng.normal(size=(len(centers), n)), axis=1)
src = np.exp(0.6 * slow) * car
J = np.zeros((len(xg), n))
for c, s in zip(centers, src):
    J[np.argmin(np.abs(xg - c))] = s / s.std()
J += 0.15 * sosfiltfilt(band, rng.normal(size=J.shape), axis=1) / 0.3   # 약한 배경 활동
Y = L @ J + 0.02 * rng.normal(size=(len(xs), n))
Jh = K @ Y
roi_ts = np.array([Jh[r].mean(axis=0) for r in rois])


def smooth(e):
    return np.fft.irfft(np.fft.rfft(e) * (fr < 0.5), n)


def aec(a, b):
    return np.corrcoef(smooth(np.abs(hilbert(a))), smooth(np.abs(hilbert(b))))[0, 1]


k0 = np.argmin(np.abs(xg - 0))
psf = R[:, k0] / R[:, k0].max()
U, _, Vt = np.linalg.svd(roi_ts, full_matrices=False)
orth = U @ Vt
true_env = [aec(src[0], src[k]) for k in range(1, 6)]
raw = [aec(roi_ts[0], roi_ts[k]) for k in range(1, 6)]
cor = [aec(orth[0], orth[k]) for k in range(1, 6)]
zl = [np.corrcoef(roi_ts[0], roi_ts[k])[0, 1] for k in range(1, 6)]
half = xg[psf >= 0.5]
print(f"PSF 반치폭 ≈ {half.max() - half.min() + 0.25:.2f} cm", file=sys.stderr)
for d, t0, r0, c0, z0 in zip(centers[1:], true_env, raw, cor, zl):
    print(f"거리 {d} cm: 실제 AEC={t0:.2f}, 원래 AEC={r0:.2f}, 대칭 직교화 AEC={c0:.2f}, 지연 0 상관={z0:.2f}",
          file=sys.stderr)

fig, (a, b) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1.2, 1], wspace=0.3))
for c, r in zip(centers, rois):
    a.axvspan(c - 0.48, c + 0.48, color="#d6e2f0" if c == 0 else C["light"], zorder=0, lw=0)
    a.text(c, -0.21, f"ROI {c}" if c == 0 else f"{c}", ha="center", fontsize=7, color=C["gray"])
k0 = np.argmin(np.abs(xg - 0))
psf = R[:, k0] / R[:, k0].max()
a.plot(xg, psf, color=C["blue"], lw=1.8, label="0 cm 점 소스의 추정 지도")
k2 = np.argmin(np.abs(xg - 3))
a.plot(xg, R[:, k2] / R[:, k2].max(), color=C["purple"], lw=1.3, ls="--", label="3 cm 점 소스")
a.axhline(0, color=C["gray"], lw=0.5)
a.set_xlim(-3, 7.5)
a.set_ylim(-0.25, 1.15)
a.set_xlabel("피질 위 위치 (cm)")
a.set_ylabel("추정 크기 (최댓값 = 1)")
a.legend(fontsize=7.3, loc="upper right", bbox_to_anchor=(1.03, 1.0))
a.set_title("(가) 점 소스가 이웃 ROI로 번진다", fontsize=9.5)
ds = centers[1:]
b.plot(ds, true_env, "D:", color=C["gray"], ms=4, lw=1.0, label="실제 소스")
b.plot(ds, raw, "o-", color=C["red"], ms=4, lw=1.4, label="ROI 시계열, 원래")
b.plot(ds, cor, "s--", color=C["blue"], ms=4, lw=1.3, mfc="white", label="대칭 직교화 뒤")
b.axhline(0, color=C["gray"], lw=0.5)
b.annotate("실제 결합\n(4 cm)", xy=(4, true_env[3]), xytext=(4.3, 0.8), fontsize=7.5,
           arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.7))
b.set_xticks(ds)
b.set_xlabel("0 cm ROI와의 거리 (cm)")
b.set_ylabel("포락선 상관")
b.set_ylim(-0.15, 1.0)
b.legend(fontsize=7.3, loc="upper left", bbox_to_anchor=(0.12, 1.0))
b.set_title("(나) 이웃일수록 가짜 결합이 크다", fontsize=9.5)
save(fig, __file__)
