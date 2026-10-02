from scipy import stats

from figstyle import plt, np, C, save

# 참 상관 r = 0.1인 뇌-행동 연관을 여러 표본 크기에서 다시 뽑는다(BWAS의 표본 변동).
rng = np.random.default_rng(22)
rho = 0.1
NS = np.array([25, 50, 100, 200, 500, 1000, 2000, 4000])
REP = 4000
rs = {}
for n in NS:
    x = rng.standard_normal((REP, n))
    y = rho * x + np.sqrt(1 - rho ** 2) * rng.standard_normal((REP, n))
    xc = x - x.mean(1, keepdims=True); yc = y - y.mean(1, keepdims=True)
    rs[n] = (xc * yc).sum(1) / np.sqrt((xc ** 2).sum(1) * (yc ** 2).sum(1))

rcrit = {n: stats.t.ppf(0.975, n - 2) / np.sqrt(n - 2 + stats.t.ppf(0.975, n - 2) ** 2) for n in NS}
lo = np.array([np.percentile(rs[n], 2.5) for n in NS])
hi = np.array([np.percentile(rs[n], 97.5) for n in NS])
power = np.array([np.mean(rs[n] > rcrit[n]) for n in NS])
winner = np.array([rs[n][rs[n] > rcrit[n]].mean() for n in NS])
for n, a, b, pw, w in zip(NS, lo, hi, power, winner):
    print(n, "95%% 범위 [%.3f, %.3f], 검정력(양측 .05, 양의 방향) %.3f, 유의한 r 평균 %.3f, 부풀림 %.1f배"
          % (a, b, pw, w, w / rho))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
for n in NS:
    sub = rs[n][:300]
    jit = np.exp(rng.uniform(-0.12, 0.12, sub.size))
    sig = sub > rcrit[n]
    a1.scatter(n * jit[~sig], sub[~sig], s=2, color=C["gray"], alpha=0.3, lw=0)
    a1.scatter(n * jit[sig], sub[sig], s=3, color=C["red"], alpha=0.7, lw=0)
a1.fill_between(NS, lo, hi, color=C["blue"], alpha=0.15, lw=0)
a1.plot(NS, [rcrit[n] for n in NS], color=C["red"], lw=0.9, ls="--")
a1.text(30, 0.62, "유의성 문턱\n($p$ < 0.05)", fontsize=7, color=C["red"])
a1.axhline(rho, color=C["blue"], lw=1.5)
a1.text(4300, -0.62, "파란 실선: 참 r = 0.1\n파란 띠: 95 % 범위", fontsize=7.2, color=C["blue"], ha="right")
a1.axhline(0, color=C["gray"], lw=0.6)
a1.set_xscale("log")
a1.set_xticks(NS); a1.set_xticklabels(NS, fontsize=7.5); a1.minorticks_off()
a1.set_ylim(-0.75, 0.85)
a1.set_xlabel("표본 크기 (명)")
a1.set_ylabel("표본 상관계수 r")
a1.set_title("(가) 표본 r의 흩어짐", fontsize=10)

a2.plot(NS, winner, "o-", color=C["red"], ms=4, label="유의한 결과만 모은 r 평균")
a2.plot(NS, power, "s-", color=C["blue"], ms=4, label="검정력")
a2.axhline(rho, color=C["gray"], lw=0.8, ls="--")
a2.text(4000, rho + 0.03, "참값 0.1", fontsize=7.5, color=C["gray"], ha="right")
a2.set_xscale("log")
a2.set_xticks(NS); a2.set_xticklabels(NS, fontsize=7.5); a2.minorticks_off()
a2.set_ylim(0, 1.02)
a2.set_xlabel("표본 크기 (명)")
a2.set_title("(나) 승자의 저주", fontsize=10)
a2.legend(fontsize=7.5, loc="center right")
fig.tight_layout()
save(fig, __file__)
