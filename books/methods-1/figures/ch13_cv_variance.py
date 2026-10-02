from figstyle import plt, np, C, save

# 진짜 신호가 있는 데이터에서 교차 검증 정확도가 표본마다 얼마나 흔들리는지 본다(Varoquaux 2018의 요지).
rng = np.random.default_rng(2018)
p = 20
delta = 0.25                       # 특징마다 집단 평균 차 (표준편차 단위)
NS = [20, 40, 60, 100, 200, 400, 1000]
REP = 300


def sample(n):
    y = np.repeat([1.0, -1.0], n // 2)
    X = rng.standard_normal((n, p)) + 0.5 * delta * y[:, None]
    return X, y


def fit(X, y, lam=5.0):
    mu = X.mean(0)
    A = X - mu
    w = np.linalg.solve(A.T @ A + lam * np.eye(p), A.T @ y)
    return w, mu


def cv_acc(X, y, nf=5):
    idx = rng.permutation(len(y)); hit = 0
    for te in np.array_split(idx, nf):
        tr = np.setdiff1d(idx, te)
        w, mu = fit(X[tr], y[tr])
        hit += (np.sign((X[te] - mu) @ w) == y[te]).sum()
    return hit / len(y)


Xbig, ybig = sample(20000)
cvs, trues = {}, {}
for n in NS:
    c, t = [], []
    for _ in range(REP):
        X, y = sample(n)
        c.append(cv_acc(X, y))
        w, mu = fit(X, y)
        t.append(np.mean(np.sign((Xbig - mu) @ w) == ybig))
    cvs[n], trues[n] = np.array(c), np.array(t)
    err = cvs[n] - trues[n]
    print(n, "CV 평균 %.3f, 5-95%% %s, 참 일반화 평균 %.3f, 오차 95%% 반폭 %.3f" %
          (cvs[n].mean(), np.round(np.percentile(cvs[n], [5, 95]), 3), trues[n].mean(),
           np.percentile(np.abs(err), 95)))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
x = np.arange(len(NS))
for i, n in enumerate(NS):
    jit = rng.uniform(-0.18, 0.18, REP)
    a1.scatter(i + jit, cvs[n], s=2, color=C["blue"], alpha=0.25, lw=0)
    lo, hi = np.percentile(cvs[n], [2.5, 97.5])
    a1.plot([i, i], [lo, hi], color=C["ink"], lw=1.2)
    a1.scatter([i], [np.median(cvs[n])], color=C["ink"], s=10, zorder=3)
    a1.scatter([i], [trues[n].mean()], color=C["red"], marker="_", s=120, zorder=4, lw=1.8)
a1.axhline(0.5, color=C["gray"], ls="--", lw=0.8)
a1.set_xticks(x); a1.set_xticklabels(NS)
a1.set_xlabel("표본 크기 (명)")
a1.set_ylabel("5겹 교차 검증 정확도")
a1.set_ylim(0.15, 1.02)
a1.set_title("(가) 같은 모집단, 다른 표본", fontsize=10)
a1.text(6.3, 0.22, "빨간 가로줄: 그 크기에서\n훈련한 모형의 참 정확도", fontsize=7, ha="right", color=C["red"])

nn = np.array(NS)
half = [np.percentile(np.abs(cvs[n] - trues[n]), 95) for n in NS]
pbar = np.array([trues[n].mean() for n in NS])
a2.plot(nn, 100 * 1.96 * np.sqrt(pbar * (1 - pbar) / nn), color=C["gray"], ls="--", lw=1.2,
        label="이항 분포 공식 $1.96\\sqrt{p(1-p)/n}$")
a2.plot(nn, 100 * np.array(half), "o-", color=C["blue"], ms=4, label="시뮬레이션 (교차 검증 − 참값)")
a2.axhline(10, color=C["red"], lw=0.7, ls=":")
a2.text(1000, 10.8, "±10 %p", fontsize=7.5, color=C["red"], ha="right")
a2.set_xscale("log")
a2.set_xticks(NS); a2.set_xticklabels(NS); a2.minorticks_off()
a2.set_xlabel("표본 크기 (명)")
a2.set_ylabel("오차 95 % 범위 반폭 (%p)")
a2.set_title("(나) 오차 막대의 크기", fontsize=10)
a2.legend(fontsize=7, loc="upper right")
fig.tight_layout()
save(fig, __file__)
