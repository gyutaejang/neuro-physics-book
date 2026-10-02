from figstyle import plt, np, C, save

# 질환 신호는 전혀 없고 스캐너(사이트) 차이만 있는 특징. 사이트 A는 환자 75 %, 사이트 B는 25 %.
rng = np.random.default_rng(31)
p, nsite = 200, 60
LAM = 1000.0                                  # 강한 정칙화: 가장 큰 분산 방향(사이트)을 주로 쓴다
site_shift = rng.standard_normal(p) * 0.4      # 사이트 B의 특징별 평균 이동


def make():
    X, y, s = [], [], []
    for site, frac in [(0, 0.75), (1, 0.25)]:
        npat = int(nsite * frac)
        yy = np.r_[np.ones(npat), -np.ones(nsite - npat)]
        XX = rng.standard_normal((nsite, p)) + site * site_shift
        X.append(XX); y.append(yy); s.append(np.full(nsite, site))
    return np.vstack(X), np.concatenate(y), np.concatenate(s)


def fit_pred(Xtr, ytr, Xte, lam=LAM):
    mu = Xtr.mean(0)
    A = Xtr - mu
    w = A.T @ np.linalg.solve(A @ A.T + lam * np.eye(len(ytr)), ytr - ytr.mean())
    return np.sign((Xte - mu) @ w)


def bacc(y, yh):
    return 0.5 * (np.mean(yh[y > 0] > 0) + np.mean(yh[y < 0] < 0))


def random_cv(X, y, nf=5):
    idx = rng.permutation(len(y)); yh = np.zeros_like(y)
    for te in np.array_split(idx, nf):
        tr = np.setdiff1d(idx, te)
        yh[te] = fit_pred(X[tr], y[tr], X[te])
    return bacc(y, yh)


def site_out(X, y, s):
    out = []
    for t in (0, 1):
        tr, te = s != t, s == t
        out.append(bacc(y[te], fit_pred(X[tr], y[tr], X[te])))
    return np.mean(out)


def centered_cv(X, y, s, nf=5):
    """사이트 평균을 훈련 접힘에서만 구해 훈련과 시험에 똑같이 뺀다."""
    idx = rng.permutation(len(y)); yh = np.zeros_like(y)
    for te in np.array_split(idx, nf):
        tr = np.setdiff1d(idx, te)
        Xtr, Xte = X[tr].copy(), X[te].copy()
        for t in (0, 1):
            m = X[tr][s[tr] == t].mean(0)
            Xtr[s[tr] == t] -= m
            Xte[s[te] == t] -= m
        yh[te] = fit_pred(Xtr, y[tr], Xte)
    return bacc(y, yh)


res = {"rand": [], "loso": [], "cent": []}
for _ in range(200):
    X, y, s = make()
    res["rand"].append(random_cv(X, y))
    res["loso"].append(site_out(X, y, s))
    res["cent"].append(centered_cv(X, y, s))
for k, v in res.items():
    print(k, "균형 정확도 평균 %.3f, 5-95%% %s" % (np.mean(v), np.round(np.percentile(v, [5, 95]), 3)))

X, y, s = make()
# 첫 주성분 2개
Xc = X - X.mean(0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
pc = Xc @ Vt[:2].T

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1, 1.1]))
for site, mk in [(0, "o"), (1, "^")]:
    for lab, col in [(1, C["red"]), (-1, C["blue"])]:
        m = (s == site) & (y == lab)
        a1.scatter(pc[m, 0], pc[m, 1], s=14, marker=mk, facecolor="none" if lab < 0 else col,
                   edgecolor=col, lw=0.8)
a1.text(0.03, 0.97, "○ 사이트 A (환자 75 %)\n△ 사이트 B (환자 25 %)", transform=a1.transAxes,
        fontsize=7.2, va="top")
a1.text(0.97, 0.03, "채움 빨강: 환자\n빈 파랑: 대조군", transform=a1.transAxes, fontsize=7.2,
        ha="right", va="bottom")
a1.set_xlabel("주성분 1"); a1.set_ylabel("주성분 2")
a1.set_xticks([]); a1.set_yticks([])
a1.set_title("(가) 특징 공간: 사이트가 갈린다", fontsize=10)
lims = a1.get_ylim(); a1.set_ylim(lims[0], lims[1] + 0.35 * (lims[1] - lims[0]))

labels = ["무작위 5겹", "사이트 남겨\n두기", "접힘 안 사이트 중심화\n뒤 무작위 5겹"]
vals = [res["rand"], res["loso"], res["cent"]]
cols = [C["red"], C["blue"], C["blue"]]
for i, (v, c) in enumerate(zip(vals, cols)):
    a2.bar(i, np.mean(v), color=c, alpha=0.85, width=0.6)
    lo, hi = np.percentile(v, [5, 95])
    a2.plot([i, i], [lo, hi], color=C["ink"], lw=1)
    a2.text(i, hi + 0.02, "%.2f" % np.mean(v), ha="center", fontsize=8)
a2.axhline(0.5, color=C["gray"], ls="--", lw=0.9)
a2.set_xticks(range(3)); a2.set_xticklabels(labels, fontsize=7.8)
a2.set_ylim(0, 1)
a2.set_ylabel("균형 정확도")
a2.set_title("(나) 검증 방식에 따른 성능", fontsize=10)
fig.tight_layout()
save(fig, __file__)
