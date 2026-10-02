"""공간 ICA: 겹쳐 섞인 합성 네트워크 지도를 PCA와 ICA로 풀기."""
import sys

from scipy import signal

from figstyle import plt, np, save, C

rng = np.random.default_rng(3)
N = 48
yy, xx = np.mgrid[0:N, 0:N]


def blob(cx, cy, s):
    return np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * s ** 2))


# 세 개의 합성 "네트워크" 지도: 서로 일부가 겹친다
S_true = np.array([
    blob(24, 12, 4.5) + blob(24, 30, 4.5),               # 앞뒤 정중선 쌍 (디폴트 모드 비슷)
    blob(12, 22, 4.0) + blob(36, 22, 4.0),               # 좌우 대칭 쌍 (감각운동 비슷)
    blob(24, 37, 3.5) + blob(15, 41, 3.0) + blob(33, 41, 3.0),  # 뒤쪽 (시각 비슷), 첫 지도와 겹침
])
S_flat = S_true.reshape(3, -1)

T = 300  # TR 2 s, 10분
b, a = signal.butter(2, [0.01, 0.1], btype="band", fs=0.5)
tc = signal.filtfilt(b, a, rng.standard_normal((T, 3)), axis=0)
tc[:, 2] = 0.5 * tc[:, 0] + tc[:, 2]   # 시간 경과끼리는 상관해도 된다(공간 ICA)
tc /= tc.std(0)
X = tc @ S_flat + 0.35 * rng.standard_normal((T, N * N))  # 시간 x 복셀

# 공간 ICA: 복셀을 표본으로 본다
Y = X - X.mean(1, keepdims=True)
U, s, Vt = np.linalg.svd(Y, full_matrices=False)
k = 3
Z = Vt[:k] * np.sqrt(N * N)          # 백색화한 공간 성분 (k x V)
pca_maps = Vt[:k]

# 대칭 FastICA (tanh 비선형)
W = np.linalg.qr(rng.standard_normal((k, k)))[0]
for it in range(300):
    WX = W @ Z
    g, gp = np.tanh(WX), 1 - np.tanh(WX) ** 2
    Wn = (g @ Z.T) / Z.shape[1] - gp.mean(1)[:, None] * W
    u, _, vt = np.linalg.svd(Wn)
    Wn = u @ vt
    if np.max(np.abs(np.abs(np.diag(Wn @ W.T)) - 1)) < 1e-8:
        W = Wn
        break
    W = Wn
ica_maps = W @ Z


def match(est):
    """참 지도와 상관이 가장 큰 성분을 골라 순서와 부호를 맞춘다."""
    cc = np.corrcoef(np.vstack([S_flat, est]))[:3, 3:]
    out, rs, used = [], [], set()
    for i in range(3):
        order = np.argsort(-np.abs(cc[i]))
        j = next(o for o in order if o not in used)
        used.add(j)
        out.append(np.sign(cc[i, j]) * est[j])
        rs.append(abs(cc[i, j]))
    return np.array(out), rs


pca_m, r_pca = match(pca_maps)
ica_m, r_ica = match(ica_maps)
print("PCA r:", np.round(r_pca, 2), "ICA r:", np.round(r_ica, 2), "iter", it, file=sys.stderr)

fig, axes = plt.subplots(3, 3, figsize=(5.6, 5.6))
rows = [("참 지도", S_flat, None), ("PCA", pca_m, r_pca), ("공간 ICA", ica_m, r_ica)]
labels = ["성분 1", "성분 2", "성분 3"]
for i, (rname, maps, rs) in enumerate(rows):
    for j in range(3):
        ax = axes[i, j]
        m = maps[j] / np.abs(maps[j]).max()
        ax.imshow(m.reshape(N, N), cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(True)
            sp.set_color(C["gray"])
        if rs is not None:
            ax.text(N - 2, N - 2, f"r = {rs[j]:.2f}", ha="right", va="bottom", fontsize=8,
                    color=C["ink"], bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
        if j == 0:
            ax.set_ylabel(rname, fontsize=9.5)
        if i == 0:
            ax.set_title(labels[j], fontsize=9.5)
fig.subplots_adjust(wspace=0.06, hspace=0.06)
save(fig, __file__)
