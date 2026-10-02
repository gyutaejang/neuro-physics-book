from figstyle import plt, np, save, C
from scipy import stats

# 두 집단 t 검정을 1만 번 되풀이한 모의 실험. 귀무가설이 참이면 p값은 0–1에 고르게 퍼지고,
# 효과가 있으면 0 쪽에 몰린다. 몰리는 정도가 검정력이다.
rng = np.random.default_rng(11)
reps = 10000


def pvals(d, n):
    a = rng.normal(0, 1, (reps, n))
    b = rng.normal(d, 1, (reps, n))
    return stats.ttest_ind(a, b, axis=1).pvalue


cases = [(0.0, 20, "(가) 효과 없음 (d = 0)"),
         (0.5, 20, "(나) d = 0.5, 집단당 20명"),
         (0.5, 64, "(다) d = 0.5, 집단당 64명")]
fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9), sharey=True)
bins = np.linspace(0, 1, 21)
for ax, (d, n, title) in zip(axes, cases):
    p = pvals(d, n)
    h, _ = np.histogram(p, bins)
    h = h / reps * 100
    cols = [C["red"]] + [C["blue"]] * 19
    ax.bar(bins[:-1], h, width=0.05, align="edge", color=cols, edgecolor="white", lw=0.4)
    ax.axhline(5, color=C["gray"], lw=0.7, ls=":")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("p값")
    ax.set_xticks([0, 0.5, 1])
    frac = (p < 0.05).mean() * 100
    ax.text(0.16, 0.93, f"p < 0.05인 비율 {frac:.0f} %", transform=ax.transAxes, fontsize=8,
            color=C["red"], va="top")
    ax.set_ylim(0, 85)
    ax.set_xlim(-0.03, 1.03)
axes[0].text(0.55, 7, "고르게 5 %씩", fontsize=7.5, color=C["gray"])
axes[0].set_ylabel("모의 실험 비율 (%)")
fig.tight_layout()
save(fig, __file__)
