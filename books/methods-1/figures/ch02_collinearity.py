from figstyle import plt, np, save, C

# (가) 두 회귀자의 상관 r이 커질수록 β의 표준오차가 √VIF = 1/√(1−r²)배로 커진다 (모의 실험 + 식)
# (나) 직교화의 기하: x₂를 x₁에 대해 직교화하면 공유 성분(회색 점선)이 x₁의 몫이 된다.
rng = np.random.default_rng(8)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2))
rs = np.linspace(0, 0.95, 200)
ax1.plot(rs, 1 / np.sqrt(1 - rs ** 2), color=C["red"], lw=1.6, label="1/√(1 − r²)")
n, reps = 100, 3000
r_sim = np.array([0, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95])
base = None
ratio = []
for r in r_sim:
    z1 = rng.normal(size=(reps, n))
    z2 = r * z1 + np.sqrt(1 - r ** 2) * rng.normal(size=(reps, n))
    e = rng.normal(size=(reps, n))
    y = 0.5 * z1 + 0.5 * z2 + e
    b1 = []
    for i in range(reps):
        X = np.c_[np.ones(n), z1[i], z2[i]]
        b1.append(np.linalg.lstsq(X, y[i], rcond=None)[0][1])
    sd = np.std(b1)
    base = sd if base is None else base
    ratio.append(sd / base)
ax1.plot(r_sim, ratio, "o", color=C["blue"], ms=4, label="모의 실험")
ax1.set_xlabel("두 회귀자 사이 상관 r")
ax1.set_ylabel("$\\beta_1$ 표준오차 (r = 0 대비 배수)")
ax1.set_title("(가) 공선성은 추정을 흔든다", fontsize=9.5)
ax1.legend(fontsize=8, loc="upper left")
ax1.set_xlim(0, 1)
ax1.set_ylim(0.9, 3.6)

x1 = np.array([1.0, 0.0])
x2 = np.array([0.8, 0.6])
proj = x2 @ x1 * x1
x2o = x2 - proj
kw = dict(arrowstyle="-|>", lw=1.6, mutation_scale=12)
ax2.annotate("", xy=x1 * 1.25, xytext=(0, 0), arrowprops=dict(color=C["blue"], **kw))
ax2.annotate("", xy=x2 * 1.25, xytext=(0, 0), arrowprops=dict(color=C["purple"], **kw))
ax2.annotate("", xy=x2o * 1.25, xytext=(0, 0), arrowprops=dict(color=C["red"], **kw))
ax2.plot([x2[0] * 1.25, proj[0] * 1.25], [x2[1] * 1.25, 0], color=C["gray"], ls=":", lw=1)
ax2.plot([0, proj[0] * 1.25], [-0.03, -0.03], color=C["gray"], lw=3, alpha=0.5)
ax2.text(1.28, -0.02, "$x_1$ (예: 과제)", fontsize=8.5, color=C["blue"], va="center")
ax2.text(1.03, 0.78, "$x_2$ (예: 반응 시간)", fontsize=8.5, color=C["purple"])
ax2.text(0.04, 0.80, "$x_2$를 $x_1$에 대해\n직교화한 것", fontsize=8.5, color=C["red"])
ax2.text(0.5, -0.12, "공유 성분: $x_1$의 몫이 된다", fontsize=8, color=C["gray"], ha="center", va="top")
ax2.set_xlim(-0.15, 1.95)
ax2.set_ylim(-0.3, 1.05)
ax2.set_aspect("equal")
ax2.axis("off")
ax2.set_title("(나) 직교화는 공유 몫을 한쪽에 몰아준다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
