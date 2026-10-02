from figstyle import plt, np, C, save

# 학습 곡선: 연결성 특징 500개로 행동 점수를 예측한다. 참 신호가 설명하는 분산은 20 %.
rng = np.random.default_rng(42)
p, R2_true = 500, 0.20
w = rng.standard_normal(p)
w *= np.sqrt(R2_true / (w @ w))            # 특징 분산 1 → 신호 분산 = R2_true
NS = [50, 100, 200, 500, 1000, 2000, 5000, 10000]
LAMS = np.logspace(0, 5, 21)
REP = 8


def draw(n, rel):
    X = rng.standard_normal((n, p))
    true = X @ w + np.sqrt(1 - R2_true) * rng.standard_normal(n)        # 분산 1인 '참 행동'
    # 측정 신뢰도 rel: 관측 점수 = 참 점수 + 측정 오차, 관측 분산 중 참 분산의 비율이 rel
    obs = true + np.sqrt((1 - rel) / rel) * rng.standard_normal(n)
    return X, obs


def ridge_path(X, y, lams):
    """λ 여러 개의 능형 회귀 해를 고윳값 분해 한 번으로 구한다."""
    mu, my = X.mean(0), y.mean()
    A = X - mu
    ev, V = np.linalg.eigh(A.T @ A)
    z = V.T @ (A.T @ (y - my))
    return [(V @ (z / (ev + lam)), mu, my) for lam in lams]


def r2(y, yh):
    return 1 - np.sum((y - yh) ** 2) / np.sum((y - y.mean()) ** 2)


out = {}
for rel in (1.0, 0.5):
    Xte, yte = draw(5000, rel)
    tr_m, te_m = [], []
    for n in NS:
        trs, tes = [], []
        for _ in range(REP):
            X, y = draw(n, rel)
            k = int(0.8 * n)                          # 안쪽 검증으로 λ 고르기
            sc = [r2(y[k:], (X[k:] - mu) @ b + my) for b, mu, my in ridge_path(X[:k], y[:k], LAMS)]
            b, mu, my = ridge_path(X, y, [LAMS[int(np.argmax(sc))]])[0]
            trs.append(r2(y, (X - mu) @ b + my))
            tes.append(r2(yte, (Xte - mu) @ b + my))
        tr_m.append(np.mean(trs)); te_m.append(np.mean(tes))
    out[rel] = (np.array(tr_m), np.array(te_m))
    print("신뢰도", rel, "훈련", np.round(out[rel][0], 3), "시험", np.round(out[rel][1], 3))

fig, ax = plt.subplots(figsize=(6.6, 3.2))
for rel, col, lab in [(1.0, C["blue"], "행동 측정 신뢰도 1.0"), (0.5, C["red"], "신뢰도 0.5")]:
    tr, te = out[rel]
    ax.plot(NS, te, "o-", color=col, ms=4, lw=1.8, label=lab + ": 새 데이터")
    ax.plot(NS, tr, "o--", color=col, ms=3, lw=1, alpha=0.6, label=lab + ": 훈련 데이터")
    ax.axhline(R2_true * rel, color=col, lw=0.7, ls=":")
ax.text(44, 0.205, "상한 0.20", fontsize=7.5, color=C["blue"], va="bottom")
ax.text(44, 0.105, "상한 0.10", fontsize=7.5, color=C["red"], va="bottom")
ax.axhline(0, color=C["gray"], lw=0.6)
ax.set_xscale("log")
ax.set_xticks(NS); ax.set_xticklabels(NS); ax.minorticks_off()
ax.set_xlim(40, 13000)
ax.set_xlabel("훈련 표본 크기 (명)")
ax.set_ylabel("설명된 분산 $R^2$")
ax.legend(fontsize=7.3, loc="upper right", ncol=2)
ax.set_ylim(-0.05, 0.75)
fig.tight_layout()
save(fig, __file__)
