from figstyle import plt, np, C, save

# 순수 잡음 "뇌 특징"으로 환자/대조군을 분류한다. 정답 정확도는 50 %다.
rng = np.random.default_rng(13)
n, k = 40, 50
y = np.repeat([1.0, -1.0], n // 2)


def top_k(X, y, k):
    m1, m0 = X[y > 0].mean(0), X[y < 0].mean(0)
    s = np.sqrt(X[y > 0].var(0, ddof=1) / (y > 0).sum() + X[y < 0].var(0, ddof=1) / (y < 0).sum())
    return np.argsort(-np.abs((m1 - m0) / s))[:k]


def cv_acc(X, y, leak, nf=5, lam=1.0):
    idx = rng.permutation(len(y))
    sel_all = top_k(X, y, k) if leak else None
    hit = 0
    for te in np.array_split(idx, nf):
        tr = np.setdiff1d(idx, te)
        s = sel_all if leak else top_k(X[tr], y[tr], k)
        mu = X[tr][:, s].mean(0)
        Xs = X[tr][:, s] - mu
        w = Xs.T @ np.linalg.solve(Xs @ Xs.T + lam * np.eye(len(tr)), y[tr])
        hit += (np.sign((X[te][:, s] - mu) @ w) == y[te]).sum()
    return hit / len(y)


p = 5000
leak, proper = [], []
for _ in range(200):
    X = rng.standard_normal((n, p))
    leak.append(cv_acc(X, y, True))
    proper.append(cv_acc(X, y, False))
leak, proper = np.array(leak), np.array(proper)
print("p=5000 누설 평균 %.3f, 올바른 평균 %.3f, 5-95%% %s" %
      (leak.mean(), proper.mean(), np.percentile(proper, [5, 95])))

ps = [50, 100, 300, 1000, 3000, 10000]
lm, lsd = [], []
for pp in ps:
    a = np.array([cv_acc(rng.standard_normal((n, pp)), y, True) for _ in range(60)])
    lm.append(a.mean()); lsd.append(a.std())
    print(pp, round(a.mean(), 3))
lm, lsd = np.array(lm), np.array(lsd)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1]))
bins = np.arange(0.2, 1.0251, 0.025)
top = max(np.histogram(leak, bins)[0].max(), 60) * 1.25
a1.hist(proper, bins=bins, color=C["blue"], alpha=0.85, label="훈련 접힘 안에서 선택")
a1.hist(leak, bins=bins, color=C["red"], alpha=0.85, label="전체 데이터로 먼저 선택")
a1.axvline(0.5, ymax=0.5, color=C["gray"], ls="--", lw=1)
a1.text(0.5, 0.51 * top, "우연 수준", ha="center", va="bottom", fontsize=7.5, color=C["gray"])
a1.set_xlabel("교차 검증 정확도")
a1.set_ylabel("반복 횟수 (200번 중)")
a1.set_title("(가) 잡음 5000개, 40명", fontsize=10)
a1.set_xlim(0.2, 1.03)
a1.set_ylim(0, top)
a1.legend(fontsize=7.5, loc="upper left")

a2.fill_between(ps, lm - lsd, np.minimum(lm + lsd, 1), color=C["red"], alpha=0.18, lw=0)
a2.plot(ps, lm, "o-", color=C["red"], ms=4, label="누설 (먼저 선택)")
a2.axhline(0.5, color=C["blue"], lw=1.6, label="올바른 절차 (평균 약 0.5)")
a2.set_xscale("log")
a2.set_ylim(0.3, 1.02)
a2.set_xlabel("후보 특징 수 (상위 50개 선택)")
a2.set_ylabel("평균 정확도")
a2.set_title("(나) 후보가 많을수록 더 부푼다", fontsize=10)
a2.legend(fontsize=7.5, loc="lower right")
fig.tight_layout()
save(fig, __file__)
