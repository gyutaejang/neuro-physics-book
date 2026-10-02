from figstyle import plt, np, save, C

# 같은 사람 40명을 두 번 측정한 합성 데이터. 사람 사이 분산과 측정 오차 분산의 비가 ICC를 정한다.
rng = np.random.default_rng(3)
n = 40


def sim(sb, sw):
    true = rng.normal(0, sb, n)
    s1 = true + rng.normal(0, sw, n)
    s2 = true + rng.normal(0, sw, n)
    return s1, s2


def icc1(s1, s2):
    # 일원 분산분석 ICC(1,1)
    y = np.c_[s1, s2]
    k = 2
    msb = k * y.mean(axis=1).var(ddof=1)
    msw = ((y - y.mean(axis=1, keepdims=True)) ** 2).sum() / (n * (k - 1))
    return (msb - msw) / (msb + (k - 1) * msw)


fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.3))
cases = [(0.30, 0.10, "(가) 사람 차이가 오차보다 크다", "참 ICC = 0.90"),
         (0.30, 0.40, "(나) 오차가 사람 차이보다 크다", "참 ICC = 0.36")]
for ax, (sb, sw, title, lab) in zip(axes, cases):
    s1, s2 = sim(sb, sw)
    s1, s2 = s1 + 0.5, s2 + 0.5
    ax.plot([-0.8, 1.8], [-0.8, 1.8], color=C["gray"], lw=0.8, ls="--")
    ax.scatter(s1, s2, s=16, color=C["blue"], alpha=0.85, zorder=3)
    ax.set_xlim(-0.8, 1.8)
    ax.set_ylim(-0.8, 1.8)
    ax.set_aspect("equal")
    ax.set_xlabel("1회차 측정값")
    ax.set_title(title, fontsize=9.5)
    ax.text(0.04, 0.96, f"{lab}\n표본 ICC = {icc1(s1, s2):.2f}", transform=ax.transAxes,
            va="top", fontsize=8.5)
    ax.text(1.75, 1.55, "같은 값", fontsize=7.5, color=C["gray"], ha="right", rotation=45)
axes[0].set_ylabel("2회차 측정값")
fig.tight_layout()
save(fig, __file__)
