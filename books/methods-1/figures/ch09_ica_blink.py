from scipy import signal

from figstyle import plt, np, save, C

rng = np.random.default_rng(7)
fs = 250.0
t = np.arange(0, 60, 1 / fs)   # 60 s를 기록하고 앞 10 s만 그린다
n = t.size


def pink(n):
    """1/f 잡음: 백색 잡음의 스펙트럼을 1/sqrt(f)로 눌러 만든다."""
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / fs)
    X[1:] /= np.sqrt(f[1:])
    X[0] = 0
    y = np.fft.irfft(X, n)
    return y / y.std()


# 원천 신호 6개
blink = np.zeros(n)
for tb in [1.5, 4.2, 7.0, 8.8] + list(np.arange(11, 60, 3.1)):
    s = np.clip(t - tb, 0, None)
    blink += (s / 0.08) ** 2 * np.exp(-s / 0.08) / (4 * np.exp(-2))
bb, ab = signal.butter(4, [20, 100], "band", fs=fs)
emg = signal.lfilter(bb, ab, rng.standard_normal(n))
emg *= np.exp(-0.5 * ((t - 6.0) / 0.35) ** 6)
emg /= emg.std() * 3
alpha = np.sin(2 * np.pi * 10.2 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t))
S = np.vstack([blink, emg, alpha, pink(n), pink(n), pink(n)])
src_names = ["깜빡임", "근전도", "알파", "배경1", "배경2", "배경3"]

# 섞는 행렬: 채널(행) × 원천(열), 단위 μV
chs = ["Fp1", "Fp2", "Fz", "T7", "Cz", "O1"]
A = np.array([
    # 깜빡임 근전도 알파 배경1 배경2 배경3
    [120, 1, 0.5, 6, 2, 1],
    [115, 1, 0.5, 5, 3, 1],
    [60, 2, 1.0, 5, 4, 2],
    [8, 14, 2.0, 2, 4, 5],
    [20, 2, 4.0, 3, 6, 3],
    [2, 1, 12.0, 2, 3, 6],
])
X = A @ S


def fastica(X, n_iter=300, seed=0):
    """대칭 FastICA (비선형 함수 tanh). X: 채널 × 시점."""
    Xc = X - X.mean(1, keepdims=True)
    d, E = np.linalg.eigh(np.cov(Xc))
    K = E @ np.diag(d ** -0.5) @ E.T          # 백색화 행렬
    Z = K @ Xc
    W = np.random.default_rng(seed).standard_normal((len(X), len(X)))
    for _ in range(n_iter):
        G = np.tanh(W @ Z)
        W_new = G @ Z.T / Z.shape[1] - np.diag((1 - G ** 2).mean(1)) @ W
        u, s, vt = np.linalg.svd(W_new)
        W = u @ vt                             # 성분끼리 직교하게 되돌린다
    unmix = W @ K
    return unmix, np.linalg.inv(unmix)


Wun, Amix = fastica(X)
Sh = Wun @ (X - X.mean(1, keepdims=True))
# 성분 순서: 첨도(뾰족함)가 큰 것부터
kurt = ((Sh - Sh.mean(1, keepdims=True)) ** 4).mean(1) / Sh.var(1) ** 2 - 3
order = np.argsort(-kurt)
Sh, Amix, kurt = Sh[order], Amix[:, order], kurt[order]
# 깜빡임 성분: 앞이마(Fp1, Fp2) 가중치가 가장 큰 성분
ib = int(np.argmax(np.abs(Amix[:2]).sum(0) / np.abs(Amix).sum(0)))
keep = [k for k in range(len(X)) if k != ib]
Xclean = Amix[:, keep] @ Sh[keep] + X.mean(1, keepdims=True)

fig = plt.figure(figsize=(7.4, 3.7))
gs = fig.add_gridspec(1, 3, wspace=0.3)
titles = ["(가) 기록된 EEG", "(나) ICA 성분 (첨도 순)", "(다) 깜빡임 성분을 뺀 EEG"]
v = t < 10
for j, (title, D) in enumerate(zip(titles, [X, Sh, Xclean])):
    ax = fig.add_subplot(gs[0, j])
    D = D[:, v]
    for k in range(6):
        y = D[k] - D[k].mean()
        if j == 1:
            y = y / (np.abs(y).max() + 1e-9) * 0.42
            col = C["red"] if k == ib else C["blue"]
            lab = f"성분 {k + 1}"
        else:
            y = y / 160.0
            col = C["blue"]
            lab = chs[k]
            if j == 2:
                ax.plot(t[v], (X[k, v] - X[k].mean()) / 160.0 - k, color=C["gray"], lw=0.5, alpha=0.5)
        ax.plot(t[v], y - k, color=col, lw=0.6)
        ax.text(-0.25, -k, lab, ha="right", va="center", fontsize=7.5,
                color=C["red"] if (j == 1 and k == ib) else C["ink"])
    ax.set_xlim(0, 10)
    ax.set_ylim(-5.7, 0.9)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("시간 (s)")
    ax.set_title(title, fontsize=9.2)
    if j == 0:
        ax.plot([9.8, 9.8], [-5.6, -5.6 + 100 / 160], color=C["ink"], lw=1.2)
        ax.text(9.65, -5.3, "100 μV", ha="right", va="center", fontsize=7)
    if j == 1:
        ax.text(2.6, -ib + 0.5, "깜빡임 성분", fontsize=7.5, color=C["red"], ha="center")

save(fig, __file__)

