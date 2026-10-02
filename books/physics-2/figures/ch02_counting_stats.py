import math

from figstyle import plt, np, save, C

rng = np.random.default_rng(2)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1.3, 1]))

# (가) 같은 측정을 2000번 되풀이했을 때 센 개수의 분포
for m, col in ((4, C["red"]), (25, C["blue"]), (100, C["purple"])):
    x = rng.poisson(m, 2000)
    k = np.arange(0, 141)
    h = np.bincount(x, minlength=k.size)[: k.size] / x.size
    a2_ = a1.bar(k, h, width=1.0, color=col, alpha=0.35, lw=0)
    pmf = np.exp(k * np.log(m) - m - np.array([math.lgamma(i + 1) for i in k]))
    a1.plot(k, pmf, color=col, lw=1.3)
    a1.text(m, pmf.max() + 0.012, f"평균 {m}\nσ = {math.sqrt(m):.0f}", ha="center", fontsize=8, color=col)
a1.set_xlim(-2, 135)
a1.set_ylim(0, 0.26)
a1.set_xlabel("한 번 측정에서 센 개수 N")
a1.set_ylabel("비율")
a1.set_title("(가) 포아송 분포: 평균이 커지면 넓어진다", fontsize=9.5)
a1.text(70, 0.2, "막대: 모의 측정 2000번\n선: 포아송 분포", fontsize=8, color=C["gray"])

# (나) 상대 잡음 σ/평균
means = np.array([3, 10, 30, 100, 300, 1000, 3000, 10000, 30000])
rel = [rng.poisson(m, 4000).std() / m for m in means]
mm = np.logspace(0, 5, 100)
a2.loglog(mm, 1 / np.sqrt(mm), color=C["blue"], lw=1.6, label="1/√N")
a2.scatter(means, rel, s=18, color=C["red"], zorder=3, label="모의 측정")
for m, lab in ((100, "100개: 10%"), (10000, "1만 개: 1%")):
    a2.annotate(lab, xy=(m, 1 / math.sqrt(m)), xytext=(m * 1.6, 1.9 / math.sqrt(m)), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.set_xlabel("평균 개수 N")
a2.set_ylabel("상대 잡음 σ / N")
a2.set_xlim(1, 1e5)
a2.legend(fontsize=8, loc="lower left")
a2.set_title("(나) 상대 잡음은 1/√N", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
