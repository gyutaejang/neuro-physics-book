from figstyle import plt, np, save, C
from scipy import stats

# 같은 실험을 30번 되풀이: 25명, 참 평균 0.5 % 신호 변화, 사람 사이 표준편차 0.6 %.
rng = np.random.default_rng(21)
mu, sd, n, reps = 0.5, 0.6, 25, 30
x = rng.normal(mu, sd, (reps, n))
m = x.mean(axis=1)
se = x.std(axis=1, ddof=1) / np.sqrt(n)
tc = stats.t.ppf(0.975, n - 1)
lo, hi = m - tc * se, m + tc * se
miss = (lo > mu) | (hi < mu)

fig, ax = plt.subplots(figsize=(6.6, 3.0))
for i in range(reps):
    col = C["red"] if miss[i] else C["blue"]
    ax.plot([i + 1, i + 1], [lo[i], hi[i]], color=col, lw=1.6)
    ax.plot(i + 1, m[i], "o", color=col, ms=3.5)
ax.plot([0, reps + 0.7], [mu, mu], color=C["ink"], lw=0.9, ls="--")
ax.axhline(0, color=C["gray"], lw=0.6)
ax.text(reps + 1.0, mu, "참 평균\n0.5 %", fontsize=8, va="center")
ax.set_xlim(0, reps + 4.5)
ax.set_xlabel("되풀이한 실험 번호")
ax.set_ylabel("% 신호 변화")
ax.text(1, 1.13, f"95 % 신뢰 구간 30개 중 {miss.sum()}개(빨강)가 참값을 놓쳤다",
        fontsize=8.5, color=C["red"])
ax.set_ylim(-0.1, 1.22)
fig.tight_layout()
save(fig, __file__)
