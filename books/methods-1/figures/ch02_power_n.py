from figstyle import plt, np, save, C
from scipy import stats

# (가) 두 집단 t 검정의 검정력 (양측 α = 0.05, 비중심 t 분포로 정확히 계산)
# (나) 참 효과 d = 0.5일 때 유의한 결과만 모으면 효과 크기가 얼마나 부풀려지는가 (모의 실험)


def power(d, n, a=0.05):
    df = 2 * n - 2
    nc = d * np.sqrt(n / 2)
    tc = stats.t.ppf(1 - a / 2, df)
    return 1 - stats.nct.cdf(tc, df, nc) + stats.nct.cdf(-tc, df, nc)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2))
ns = np.arange(5, 401)
for d, col in [(0.8, C["green"]), (0.5, C["blue"]), (0.2, C["purple"])]:
    pw = power(d, ns)
    n80 = ns[np.argmax(pw >= 0.8)]
    ax1.plot(ns, pw, color=col, lw=1.6, label=f"d = {d} ({n80}명)")
    ax1.plot([n80], [0.8], "o", color=col, ms=4)
ax1.axhline(0.8, color=C["gray"], lw=0.7, ls=":")
ax1.axhline(0.05, color=C["gray"], lw=0.7, ls=":")
ax1.text(400, 0.07, "α = 0.05", fontsize=7.5, color=C["gray"], ha="right")
ax1.set_xscale("log")
ax1.set_xticks([5, 10, 20, 50, 100, 200, 400])
ax1.set_xticklabels(["5", "10", "20", "50", "100", "200", "400"])
ax1.minorticks_off()
ax1.set_xlim(5, 400)
ax1.set_ylim(0, 1.22)
ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax1.legend(fontsize=7.5, loc="upper center", ncol=3, handlelength=1.2, columnspacing=0.8)
ax1.set_xlabel("집단당 표본 수 n")
ax1.set_ylabel("검정력")
ax1.set_title("(가) 검정력 80 %에 필요한 n", fontsize=9.5)

rng = np.random.default_rng(5)
d_true = 0.5
nlist = np.array([10, 15, 20, 30, 45, 64, 100, 150])
mean_sig, mean_all = [], []
for n in nlist:
    a = rng.normal(0, 1, (20000, n))
    b = rng.normal(d_true, 1, (20000, n))
    sp = np.sqrt((a.var(axis=1, ddof=1) + b.var(axis=1, ddof=1)) / 2)
    dh = (b.mean(axis=1) - a.mean(axis=1)) / sp
    p = stats.ttest_ind(a, b, axis=1).pvalue
    sig = (p < 0.05) & (dh > 0)
    mean_sig.append(dh[sig].mean())
    mean_all.append(dh.mean())
ax2.plot(nlist, mean_sig, "o-", color=C["red"], ms=4, lw=1.4, label="유의한 결과만의 평균")
ax2.plot(nlist, mean_all, "s-", color=C["blue"], ms=3.5, lw=1.0, label="모든 결과의 평균")
ax2.axhline(d_true, color=C["gray"], lw=0.7, ls="--")
ax2.text(150, d_true - 0.05, "참 효과 0.5", fontsize=7.5, color=C["gray"], ha="right", va="top")
ax2.set_xscale("log")
ax2.set_xticks([10, 20, 50, 100, 150])
ax2.set_xticklabels(["10", "20", "50", "100", "150"])
ax2.minorticks_off()
ax2.set_ylim(0, 1.4)
ax2.set_xlabel("집단당 표본 수 n")
ax2.set_ylabel("추정한 효과 크기 d")
ax2.set_title("(나) 작은 표본의 유의한 효과는 부풀려진다", fontsize=9.5)
ax2.legend(fontsize=7.5, loc="upper right")
fig.tight_layout()
save(fig, __file__)
