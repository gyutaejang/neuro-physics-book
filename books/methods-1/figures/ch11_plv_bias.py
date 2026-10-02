import sys

from figstyle import plt, np, save, C

# PLV의 표본 편향. 위상차가 완전히 무작위(실제 결합 0)여도 시행 N개의 PLV는 0이 아니다.
# 기댓값은 대략 sqrt(pi / (4N)). 쌍 위상 일관성(PPC)은 이 편향을 없앤 추정량이다.
rng = np.random.default_rng(7)
rep = 20000


def plv(phi):
    return np.abs(np.exp(1j * phi).mean(axis=-1))


fig, (a, b) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(wspace=0.3))
bins = np.linspace(0, 0.8, 41)
for N, col in ((10, C["red"]), (30, C["purple"]), (100, C["blue"])):
    v = plv(rng.uniform(-np.pi, np.pi, (rep, N)))
    q95 = np.quantile(v, 0.95)
    a.hist(v, bins=bins, density=True, histtype="stepfilled", alpha=0.35, color=col)
    a.hist(v, bins=bins, density=True, histtype="step", lw=1.3, color=col, label=f"N = {N}")
    print(f"N={N}: 평균 PLV={v.mean():.3f} (이론 {np.sqrt(np.pi / 4 / N):.3f}), 95%={q95:.3f}",
          file=sys.stderr)
a.set_xlabel("PLV (실제 결합 0)")
a.set_ylabel("확률 밀도")
a.set_xlim(0, 0.8)
a.legend(fontsize=7.8, loc="upper right")
a.set_title("(가) 결합이 없어도 PLV는 0이 아니다", fontsize=9.5)

Ns = np.array([5, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300])
kappa = 0.41  # 실제 PLV가 약 0.2가 되는 폰 미제스 집중도


def stats(N, null):
    phi = rng.uniform(-np.pi, np.pi, (4000, N)) if null else rng.vonmises(0, kappa, (4000, N))
    p = plv(phi)
    ppc = (N * p**2 - 1) / (N - 1)
    return p.mean(), ppc.mean()


true_plv = np.abs(np.exp(1j * rng.vonmises(0, kappa, 2_000_000)).mean())
print(f"실제 PLV={true_plv:.3f}, 실제 PLV^2={true_plv**2:.3f}", file=sys.stderr)
r0 = np.array([stats(N, True) for N in Ns])
r1 = np.array([stats(N, False) for N in Ns])
for N, x0, x1 in zip(Ns, r0, r1):
    print(f"N={N}: 귀무 PLV={x0[0]:.3f} PPC={x0[1]:.4f} | 결합 PLV={x1[0]:.3f} PPC={x1[1]:.3f}",
          file=sys.stderr)
b.plot(Ns, r1[:, 0], "o-", color=C["blue"], ms=3.5, lw=1.4, label="PLV, 결합 0.2")
b.plot(Ns, r0[:, 0], "o-", color=C["red"], ms=3.5, lw=1.4, label="PLV, 결합 없음")
b.plot(Ns, np.sqrt(r1[:, 1].clip(0)), "s--", color=C["blue"], ms=3.5, lw=1.1, mfc="white",
       label="√(평균 PPC), 결합 0.2")
b.plot(Ns, np.sqrt(r0[:, 1].clip(0)), "s--", color=C["red"], ms=3.5, lw=1.1, mfc="white",
       label="√(평균 PPC), 결합 없음")
b.axhline(true_plv, color=C["gray"], lw=0.8, ls=":")
b.set_xscale("log")
b.set_xticks([5, 10, 20, 50, 100, 300])
b.set_xticklabels(["5", "10", "20", "50", "100", "300"])
b.minorticks_off()
b.set_ylim(0, 0.5)
b.set_xlabel("시행 수 N")
b.set_ylabel("평균 추정값")
b.legend(fontsize=7.3, loc="upper right")
b.set_title("(나) 시행 수에 따라 PLV가 바뀐다", fontsize=9.5)
save(fig, __file__)
