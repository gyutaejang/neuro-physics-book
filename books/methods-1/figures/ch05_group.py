from figstyle import plt, np, save, C
from scipy import stats

# 2수준 요약 통계 방법: 피험자마다 대비 추정값 하나를 집단 수준 t 검정에 넣는다.
mu, sb, sw = 0.4, 0.6, 0.3          # 집단 평균, 피험자 간 SD, 피험자 내 표준오차(% 신호 변화)
n = 20
rng = np.random.default_rng(11)
true_i = mu + sb * rng.standard_normal(n)
se_i = sw * rng.uniform(0.7, 1.4, n)
b_i = true_i + se_i * rng.standard_normal(n)

m_rfx = b_i.mean()
se_rfx = b_i.std(ddof=1) / np.sqrt(n)
t_rfx = m_rfx / se_rfx
ci_rfx = stats.t.ppf(0.975, n - 1) * se_rfx
w = 1 / se_i ** 2
m_ffx = (w * b_i).sum() / w.sum()
se_ffx = 1 / np.sqrt(w.sum())
t_ffx = m_ffx / se_ffx

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.15), gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.35})
order = np.argsort(b_i)
yv = np.arange(n) + 3
a1.errorbar(b_i[order], yv, xerr=1.96 * se_i[order], fmt="o", color=C["blue"], ms=3.5,
            ecolor=C["blue"], elinewidth=0.9, capsize=0)
a1.axvline(0, color=C["gray"], lw=0.7)
a1.errorbar([m_ffx], [1.4], xerr=[1.96 * se_ffx], fmt="D", color=C["purple"], ms=5, capsize=3, lw=1.2)
a1.errorbar([m_rfx], [0.0], xerr=[ci_rfx], fmt="D", color=C["red"], ms=5, capsize=3, lw=1.2)
a1.text(1.5, 1.4, f"고정 효과  t = {t_ffx:.1f}", fontsize=7.8, color=C["purple"], va="center")
a1.text(1.5, 0.0, f"요약 통계(무작위)  t = {t_rfx:.1f}", fontsize=7.8, color=C["red"], va="center")
a1.set_yticks([])
a1.spines["left"].set_visible(False)
a1.set_xlim(-1.4, 3.6)
a1.set_ylim(-1, n + 4)
a1.set_xlabel("대비 추정값 (% 신호 변화)")
a1.set_title("(가) 피험자 20명의 1수준 결과와 집단 평균", fontsize=9.5)
a1.text(-1.35, n + 3.2, "피험자 (95 % 구간은 피험자 내 잡음만)", fontsize=7.5, color=C["blue"])

ns = np.arange(5, 61)
for k, ls, col in ((1, "-", C["blue"]), (4, "--", C["green"])):
    tt = mu / np.sqrt((sb ** 2 + sw ** 2 / k) / ns)
    a2.plot(ns, tt, ls=ls, color=col, lw=1.6, label=f"스캔 시간 {k}배 (피험자 내 SE {sw / np.sqrt(k):.2f} %)")
tt0 = mu / np.sqrt((sw ** 2) / ns)
a2.plot(ns, tt0, color=C["purple"], lw=1.0, ls=":", label="피험자 간 차이가 없다면")
crit = stats.t.ppf(0.975, ns - 1)
a2.plot(ns, crit, color=C["gray"], lw=0.9, label="양측 $p$ = 0.05 임계값")
a2.set_xlabel("피험자 수")
a2.set_ylabel("기대 집단 $t$")
a2.set_ylim(0, 8)
a2.set_xlim(5, 60)
a2.set_title("(나) 집단 $t$를 키우는 것은 피험자 수", fontsize=9.5)
a2.text(47, 5.0, "스캔 시간 4배", fontsize=7.8, color=C["green"], ha="center")
a2.text(47, 3.35, "스캔 시간 1배", fontsize=7.8, color=C["blue"], ha="center")
a2.text(29, 6.1, "피험자 간 차이가 없다면", fontsize=7.8, color=C["purple"], ha="left")
a2.text(45, 1.55, "양측 p = 0.05 임계값", fontsize=7.5, color=C["gray"], ha="center")
save(fig, __file__)
print("mean rfx", m_rfx, "sd", b_i.std(ddof=1), "se", se_rfx, "t", t_rfx, "ci", ci_rfx, "p", 2 * stats.t.sf(t_rfx, n - 1))
print("ffx", m_ffx, se_ffx, t_ffx)
for k in (1, 4):
    print(k, [mu / np.sqrt((sb ** 2 + sw ** 2 / k) / nn) for nn in (20, 40)])
