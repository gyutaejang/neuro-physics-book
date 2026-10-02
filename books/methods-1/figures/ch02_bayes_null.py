from figstyle import plt, np, save, C
from scipy import stats

# 한 집단 설계에서 유의하지 않은 두 결과. 효과 크기 d에 사전분포 N(0, 0.5²)를 두고
# 관측 d̂의 표준오차를 1/√n으로 어림한 정규-정규 모형으로 사후분포와 베이즈 인자 BF₀₁을 구한다.
tau = 0.5
cases = [(0.10, 20, "(가) n = 20, 관측 d = 0.10"), (0.05, 200, "(나) n = 200, 관측 d = 0.05")]
d = np.linspace(-1.2, 1.2, 1201)
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
for ax, (dh, n, title) in zip(axes, cases):
    se = 1 / np.sqrt(n)
    pv = 1 / (1 / tau ** 2 + 1 / se ** 2)
    pm = pv * dh / se ** 2
    prior = stats.norm.pdf(d, 0, tau)
    post = stats.norm.pdf(d, pm, np.sqrt(pv))
    bf01 = stats.norm.pdf(dh, 0, se) / stats.norm.pdf(dh, 0, np.sqrt(tau ** 2 + se ** 2))
    p = 2 * stats.norm.sf(abs(dh) / se)
    ax.fill_between(d, post, color=C["blue"], alpha=0.25)
    ax.plot(d, post, color=C["blue"], lw=1.6, label="사후분포")
    ax.plot(d, prior, color=C["gray"], lw=1.2, ls="--", label="사전분포")
    ax.axvspan(-0.2, 0.2, color=C["green"], alpha=0.10, lw=0)
    inside = stats.norm.cdf(0.2, pm, np.sqrt(pv)) - stats.norm.cdf(-0.2, pm, np.sqrt(pv))
    ax.text(0.03, 0.96, f"p = {p:.2f}\n$\\mathrm{{BF}}_{{01}}$ = {bf01:.1f}\n|d| < 0.2일 사후확률 {inside * 100:.0f} %",
            transform=ax.transAxes, fontsize=8, va="top")
    ax.set_title(title, fontsize=9.5)
    ax.set_xlabel("효과 크기 d")
    ax.set_xlim(-1.2, 1.2)
axes[0].set_ylabel("확률 밀도")
axes[1].legend(fontsize=8, loc="upper right")
fig.tight_layout()
save(fig, __file__)
