from matplotlib.patches import Rectangle

from figstyle import plt, np, C, save

# (가) 중첩 교차 검증 도식, (나) 잡음 데이터에서 '최고 설정의 점수'를 그대로 보고할 때의 낙관 편향.
rng = np.random.default_rng(7)
n, p = 40, 2000
y = np.repeat([1.0, -1.0], n // 2)
KS = [5, 10, 20, 50, 100, 200]
LAMS = [0.1, 1.0, 10.0, 100.0]


def tscore(X, y):
    m1, m0 = X[y > 0].mean(0), X[y < 0].mean(0)
    s = np.sqrt(X[y > 0].var(0, ddof=1) / (y > 0).sum() + X[y < 0].var(0, ddof=1) / (y < 0).sum())
    return np.abs((m1 - m0) / s)


def fit_predict(Xtr, ytr, Xte, k, lam, order):
    s = order[:k]
    mu = Xtr[:, s].mean(0)
    A = Xtr[:, s] - mu
    w = A.T @ np.linalg.solve(A @ A.T + lam * np.eye(len(ytr)), ytr)
    return np.sign((Xte[:, s] - mu) @ w)


def grid_cv(X, y, nf):
    """설정마다 교차 검증 정확도(특징 선택은 훈련 접힘 안에서)."""
    idx = rng.permutation(len(y))
    hits = np.zeros((len(KS), len(LAMS)))
    for te in np.array_split(idx, nf):
        tr = np.setdiff1d(idx, te)
        order = np.argsort(-tscore(X[tr], y[tr]))
        for i, k in enumerate(KS):
            for j, lam in enumerate(LAMS):
                hits[i, j] += (fit_predict(X[tr], y[tr], X[te], k, lam, order) == y[te]).sum()
    return hits / len(y)


def nested(X, y):
    idx = rng.permutation(len(y))
    hit = 0
    for te in np.array_split(idx, 5):
        tr = np.setdiff1d(idx, te)
        g = grid_cv(X[tr], y[tr], 4)
        i, j = np.unravel_index(np.argmax(g), g.shape)
        order = np.argsort(-tscore(X[tr], y[tr]))
        hit += (fit_predict(X[tr], y[tr], X[te], KS[i], LAMS[j], order) == y[te]).sum()
    return hit / len(y)


best, nest = [], []
for _ in range(100):
    X = rng.standard_normal((n, p))
    best.append(grid_cv(X, y, 5).max())
    nest.append(nested(X, y))
best, nest = np.array(best), np.array(nest)
print("비중첩 최고 평균 %.3f (5-95%% %s), 중첩 평균 %.3f" %
      (best.mean(), np.percentile(best, [5, 95]), nest.mean()))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[1.35, 1]))
# 도식
a1.set_xlim(0, 10.6); a1.set_ylim(-0.4, 6.3); a1.axis("off")
a1.set_title("(가) 중첩 교차 검증", fontsize=10)
for r in range(5):
    yy = 5.2 - r * 0.62
    for c in range(5):
        col = C["red"] if c == r else C["light"]
        a1.add_patch(Rectangle((0.3 + c * 0.9, yy), 0.86, 0.48, color=col, ec="white", lw=0.8))
    a1.text(0.2, yy + 0.24, f"바깥 {r + 1}", ha="right", va="center", fontsize=7)
a1.text(2.55, 5.85, "바깥 고리: 성능 평가", ha="center", fontsize=8, color=C["ink"])
a1.annotate("", xy=(6.25, 4.0), xytext=(4.95, 5.45),
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.9))
a1.text(8.15, 5.85, "안쪽 고리: 설정 고르기", ha="center", fontsize=8, color=C["ink"])
for r in range(4):
    yy = 4.85 - r * 0.55
    for c in range(4):
        col = C["purple"] if c == r else C["blue"]
        a1.add_patch(Rectangle((6.4 + c * 0.9, yy), 0.86, 0.42, color=col, alpha=0.75 if c != r else 0.9,
                               ec="white", lw=0.8))
a1.text(8.15, 2.35, "바깥 1의 훈련 부분만 다시 4등분", ha="center", fontsize=7, color=C["gray"])
a1.add_patch(Rectangle((0.3, 1.2), 0.5, 0.35, color=C["red"]))
a1.text(0.95, 1.37, "평가용 (끝까지 손대지 않음)", va="center", fontsize=7.5)
a1.add_patch(Rectangle((0.3, 0.65), 0.5, 0.35, color=C["purple"]))
a1.text(0.95, 0.82, "검증용 (특징 수, 정칙화 세기 고르기)", va="center", fontsize=7.5)
a1.add_patch(Rectangle((0.3, 0.1), 0.5, 0.35, color=C["blue"], alpha=0.75))
a1.text(0.95, 0.27, "훈련용 (특징 선택과 모형 적합)", va="center", fontsize=7.5)

bins = np.arange(0.2, 0.95, 0.025)
a2.hist(nest, bins=bins, color=C["blue"], alpha=0.85, label="중첩 (평균 %.2f)" % nest.mean())
a2.hist(best, bins=bins, color=C["red"], alpha=0.85, label="24개 설정 중 최고 (평균 %.2f)" % best.mean())
a2.axvline(0.5, ymax=0.78, color=C["gray"], ls="--", lw=1)
a2.set_xlabel("보고된 정확도")
a2.set_ylabel("반복 횟수 (100번 중)")
a2.set_title("(나) 잡음 데이터의 설정 고르기", fontsize=10)
a2.set_ylim(0, 40)
a2.legend(fontsize=7.2, loc="upper left")
fig.tight_layout()
save(fig, __file__)
