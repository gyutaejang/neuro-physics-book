from scipy import stats
from figstyle import plt, np, save, C

# 공동 ICA(joint ICA, Calhoun 2006) 장난감 예: 피험자마다 회백질 지도와 FDG 지도를 이어 붙인 뒤
# 두 모달이 같은 피험자 가중치(혼합 계수)를 공유한다고 가정하고 공간 ICA를 한 번에 푼다.
rng = np.random.default_rng(11)
V = 100
v = np.arange(V)
bump = lambda c, w: np.exp(-0.5 * ((v - c) / w) ** 2)
S_true = np.array([np.r_[-bump(30, 4), -0.8 * bump(68, 6)],          # 성분 1: 해마 위축 + 후대상 저대사
                   np.r_[-0.7 * bump(78, 5), -bump(22, 4)]])         # 성분 2: 전두 위축 + 후두 저대사 (집단과 무관)
N = 80
group = np.r_[np.zeros(40), np.ones(40)]
M_true = np.c_[1.0 * group + rng.normal(0, 0.35, N), rng.normal(0.5, 0.5, N)]
X = M_true @ S_true + rng.normal(0, 0.12, (N, 2 * V))
X -= X.mean(0)
X[:, :V] /= np.linalg.norm(X[:, :V])          # 모달마다 크기를 맞춘다
X[:, V:] /= np.linalg.norm(X[:, V:])

K = 2
U, s, Vt = np.linalg.svd(X, full_matrices=False)
Y = Vt[:K] * np.sqrt(2 * V)                   # 화이트닝한 공간 신호 (K × 특징)


def fastica(Y, iters=500):
    W = np.linalg.qr(rng.standard_normal((K, K)))[0]
    for _ in range(iters):
        G = np.tanh(W @ Y)
        Wn = G @ Y.T / Y.shape[1] - np.diag((1 - G ** 2).mean(1)) @ W
        u, _, vt = np.linalg.svd(Wn)
        W = u @ vt                             # 대칭 직교화
    return W


W = fastica(Y)
S_est = W @ Y
A_est = U[:, :K] * s[:K] @ np.linalg.inv(W) / np.sqrt(2 * V)
order = [np.argmax([abs(np.corrcoef(S_est[i], S_true[j])[0, 1]) for i in range(K)]) for j in range(K)]
S_est, A_est = S_est[order], A_est[:, order]
for j in range(K):
    sg = np.sign(np.corrcoef(S_est[j], S_true[j])[0, 1])
    S_est[j] *= sg
    A_est[:, j] *= sg
    S_est[j] /= np.abs(S_est[j]).max()
    A_est[:, j] = (A_est[:, j] - A_est[:, j].mean()) / A_est[:, j].std()   # 가중치는 표준점수로 나타낸다
    r = np.corrcoef(S_est[j], S_true[j])[0, 1]
    tt = stats.ttest_ind(A_est[group == 1, j], A_est[group == 0, j])
    print(f"comp{j+1}: r = {r:.3f}, group t = {tt.statistic:.1f}, p = {tt.pvalue:.2g}")

fig = plt.figure(figsize=(7.4, 3.6))
gs = fig.add_gridspec(2, 2, width_ratios=[1.7, 1], hspace=0.75, wspace=0.3)
cols = [C["red"], C["blue"]]
xx = np.arange(2 * V)
for row, (S, ttl) in enumerate([(S_true, "(가) 참 공동 성분"), (S_est, "(나) 공동 ICA가 찾은 성분")]):
    a = fig.add_subplot(gs[row, 0])
    for j in range(K):
        a.plot(xx, S[j] / np.abs(S[j]).max(), color=cols[j], lw=1.4, label=f"성분 {j + 1}")
    a.axvline(V - 0.5, color=C["gray"], lw=0.8, ls="--")
    a.text(V / 2, 0.55, "회백질 (MRI)", ha="center", fontsize=7.8, color=C["gray"])
    a.text(1.5 * V, 0.55, "FDG (PET)", ha="center", fontsize=7.8, color=C["gray"])
    a.set_ylim(-1.25, 0.95)
    a.set_xlim(0, 2 * V)
    a.set_xticks([0, 50, 100, 150, 200])
    a.set_xticklabels(["0", "50", "0", "50", "100"])
    a.set_yticks([-1, 0])
    a.set_title(ttl, fontsize=9.5)
    if row == 0:
        a.legend(fontsize=7.2, loc="lower right", ncol=2)
    else:
        a.set_xlabel("특징 번호 (복셀 또는 영역)")
a = fig.add_subplot(gs[:, 1])
for j in range(K):
    for g, mk in [(0, "o"), (1, "s")]:
        yv = A_est[group == g, j]
        xj = j + (g - 0.5) * 0.45 + rng.uniform(-0.08, 0.08, len(yv))
        a.plot(xj, yv, mk, ms=3, color=cols[j], mfc="none" if g == 0 else cols[j], alpha=0.8)
    tt = stats.ttest_ind(A_est[group == 1, j], A_est[group == 0, j])
    a.text(j, A_est[:, j].max() + 0.25, f"t = {tt.statistic:.1f}", ha="center", fontsize=7.8, color=cols[j])
a.set_xticks([-0.22, 0.22, 0.78, 1.22])
a.set_xticklabels(["대조", "환자", "대조", "환자"], fontsize=8)
a.text(0, -0.2, "성분 1", ha="center", transform=a.get_xaxis_transform(), fontsize=8.2, color=cols[0])
a.text(1, -0.2, "성분 2", ha="center", transform=a.get_xaxis_transform(), fontsize=8.2, color=cols[1])
a.set_ylabel("피험자 가중치 (표준점수)")
a.set_ylim(top=A_est.max() + 0.7)
a.set_title("(다) 공유된 피험자 가중치", fontsize=9.5)
save(fig, __file__)
