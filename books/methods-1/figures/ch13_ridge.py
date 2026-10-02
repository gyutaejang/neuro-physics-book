from figstyle import plt, np, C, save

# 능형 회귀: 뇌 특징 300개(훈련 200명)로 인지 점수를 예측한다. 진짜 신호는 넓게 퍼진 작은 가중치다.
rng = np.random.default_rng(3)
p, ntr, nte = 300, 200, 2000
w_true = rng.standard_normal(p) * 0.06
noise_sd = np.sqrt(np.sum(w_true ** 2))       # 신호 분산 = 잡음 분산 → 이론 최고 R² = 0.5
Xtr = rng.standard_normal((ntr, p)); Xte = rng.standard_normal((nte, p))
ytr = Xtr @ w_true + noise_sd * rng.standard_normal(ntr)
yte = Xte @ w_true + noise_sd * rng.standard_normal(nte)


def ridge(X, y, lam):
    return X.T @ np.linalg.solve(X @ X.T + lam * np.eye(len(y)), y)


def r2(y, yh):
    return 1 - np.sum((y - yh) ** 2) / np.sum((y - y.mean()) ** 2)


lams = np.logspace(-2, 5, 60)
tr, te = [], []
for lam in lams:
    w = ridge(Xtr, ytr, lam)
    tr.append(r2(ytr, Xtr @ w)); te.append(r2(yte, Xte @ w))
tr, te = np.array(tr), np.array(te)
ib = te.argmax()
print("최적 lambda %.0f, 시험 R2 %.3f, lambda=0.01 시험 R2 %.3f 훈련 %.3f" % (lams[ib], te[ib], te[0], tr[0]))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1.3, 1]))
a1.plot(lams, tr, color=C["gray"], lw=1.8, label="훈련 데이터 $R^2$")
a1.plot(lams, te, color=C["blue"], lw=2, label="새 데이터 $R^2$")
a1.axhline(0.5, color=C["green"], ls=":", lw=1)
a1.text(1.3e-2, 0.53, "이론 최고 0.5", fontsize=7.5, color=C["green"])
a1.axhline(0, color=C["gray"], lw=0.6)
a1.scatter([lams[ib]], [te[ib]], color=C["red"], zorder=4, s=22)
a1.annotate("최적 λ ≈ %.0f\n$R^2$ ≈ %.2f" % (lams[ib], te[ib]), xy=(lams[ib], te[ib]),
            xytext=(2.0, 0.27), fontsize=7.5, color=C["red"], ha="center",
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
a1.text(0.015, 0.83, "과적합\n(훈련만 잘 맞음)", fontsize=7.5, color=C["ink"], va="center")
a1.text(4e4, 0.34, "과소적합\n(너무 눌림)", fontsize=7.5, color=C["ink"], ha="center")
a1.set_xscale("log")
a1.set_ylim(-0.5, 1.05)
a1.set_xlabel("정칙화 세기 λ")
a1.set_ylabel("설명된 분산 $R^2$")
a1.set_title("(가) 훈련 성능과 일반화 성능", fontsize=10)
a1.legend(fontsize=7.5, loc="lower right")

for lam, col, lab in [(lams[0], C["gray"], "λ = 0.01"), (lams[ib], C["blue"], "최적 λ")]:
    w = ridge(Xtr, ytr, lam)
    a2.scatter(w_true, w * (1 if lam == lams[ib] else 1), s=5, color=col, alpha=0.6, label=lab)
a2.plot([-0.2, 0.2], [-0.2, 0.2], color=C["red"], lw=0.8, ls="--")
a2.set_xlim(-0.2, 0.2); a2.set_ylim(-0.2, 0.2)
a2.set_xlabel("참 가중치")
a2.set_ylabel("추정 가중치")
a2.set_title("(나) 가중치 추정", fontsize=10)
a2.legend(fontsize=7.5, loc="upper left", markerscale=2.5)
fig.tight_layout()
save(fig, __file__)
