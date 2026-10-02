from figstyle import plt, np, save, C

# 사람마다 시행 수가 다른 합성 데이터(12명, 시행 4–60개). 참 효과는 N(0.5, 0.3²), 시행 잡음 표준편차 1.
# 개인 평균(무풀링)과 부분 풀링(경험적 베이즈, 혼합 효과 모형의 무작위 효과 추정)을 비교한다.
rng = np.random.default_rng(14)
J = 12
mu, tau, sig = 0.5, 0.3, 1.0
ntr = np.array([4, 5, 6, 8, 10, 12, 15, 20, 25, 35, 45, 60])
theta = rng.normal(mu, tau, J)
raw = np.array([rng.normal(th, sig, n).mean() for th, n in zip(theta, ntr)])
w = tau ** 2 / (tau ** 2 + sig ** 2 / ntr)
grand = np.sum(raw / (tau ** 2 + sig ** 2 / ntr)) / np.sum(1 / (tau ** 2 + sig ** 2 / ntr))
shr = w * raw + (1 - w) * grand

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw=dict(width_ratios=[1.3, 1]))
for j in range(J):
    ax1.annotate("", xy=(1, shr[j]), xytext=(0, raw[j]),
                 arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=0.7, mutation_scale=8))
ax1.scatter(np.zeros(J), raw, s=ntr * 1.6 + 6, color=C["blue"], zorder=3, alpha=0.85)
ax1.scatter(np.ones(J), shr, s=ntr * 1.6 + 6, color=C["red"], zorder=3, alpha=0.85)
ax1.plot([-0.35, 1.12], [grand, grand], color=C["gray"], lw=0.7, ls="--")
ax1.text(1.15, grand, "집단 평균", fontsize=7.5, color=C["gray"], va="center")
ax1.set_xticks([0, 1])
ax1.set_xticklabels(["개인 평균\n(따로 추정)", "혼합 효과\n(부분 풀링)"])
ax1.set_xlim(-0.35, 1.5)
ax1.set_ylabel("개인 효과 추정")
ax1.set_title("(가) 시행이 적은 사람일수록 많이 당겨진다", fontsize=9.5)
ax1.text(1.48, raw.min(), "점 크기 = 시행 수", fontsize=7.5,
         color=C["gray"], va="bottom", ha="right")

# (나) 오차 비교: 모의 실험 2000번의 평균 제곱근 오차
reps = 2000
err_raw = np.zeros(J)
err_shr = np.zeros(J)
for _ in range(reps):
    th = rng.normal(mu, tau, J)
    rw = th + rng.normal(0, 1, J) * sig / np.sqrt(ntr)
    g = np.sum(rw / (tau ** 2 + sig ** 2 / ntr)) / np.sum(1 / (tau ** 2 + sig ** 2 / ntr))
    sh = w * rw + (1 - w) * g
    err_raw += (rw - th) ** 2
    err_shr += (sh - th) ** 2
ax2.plot(ntr, np.sqrt(err_raw / reps), "o-", color=C["blue"], ms=4, lw=1.2, label="개인 평균")
ax2.plot(ntr, np.sqrt(err_shr / reps), "o-", color=C["red"], ms=4, lw=1.2, label="부분 풀링")
ax2.set_xscale("log")
ax2.set_xticks([4, 10, 20, 60])
ax2.set_xticklabels(["4", "10", "20", "60"])
ax2.minorticks_off()
ax2.set_xlabel("그 사람의 시행 수")
ax2.set_ylabel("참값과의 오차 (RMSE)")
ax2.set_title("(나) 당겨진 추정이 참값에 더 가깝다", fontsize=9.5)
ax2.legend(fontsize=8)
ax2.set_ylim(0, 0.55)
fig.tight_layout()
save(fig, __file__)
