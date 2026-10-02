from figstyle import plt, np, save, C

rng = np.random.default_rng(3)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))

# 왼쪽: 2차원 무작위 걸음 다섯 개
cols = [C["blue"], C["red"], C["green"], C["purple"], C["gray"]]
for c in cols:
    steps = rng.normal(0, 1, (400, 2))
    path = np.vstack([[0, 0], np.cumsum(steps, axis=0)])
    a1.plot(path[:, 0], path[:, 1], color=c, lw=0.6, alpha=0.9)
    a1.scatter(path[-1, 0], path[-1, 1], color=c, s=14, zorder=3)
a1.scatter([0], [0], color=C["ink"], s=30, zorder=4, marker="x")
r = np.sqrt(2 * 400)  # 2차원에서 제곱평균 거리 = sqrt(N) * 걸음 크기 * sqrt(2)
th = np.linspace(0, 2 * np.pi, 200)
a1.plot(r * np.cos(th), r * np.sin(th), color=C["ink"], lw=0.8, ls="--")
a1.text(0.5, 0.02, "점선 원: 제곱평균 거리 (√걸음 수에 비례)", transform=a1.transAxes, ha="center", va="bottom", fontsize=8.5)
a1.set_aspect("equal")
a1.set_xlim(-48, 48)
a1.set_ylim(-50, 46)
a1.set_xticks([])
a1.set_yticks([])
for sp in a1.spines.values():
    sp.set_visible(False)
a1.set_title("무작위 걸음 다섯 개 (각 400걸음)")

# 오른쪽: 1차원 무작위 걸음 2000개의 평균 변위와 평균제곱변위
N, n = 2000, 400
x = np.cumsum(rng.choice([-1, 1], (N, n)), axis=1)
t = np.arange(1, n + 1)
a2.plot(t, (x ** 2).mean(axis=0), color=C["blue"], lw=1.8, label=r"평균제곱변위 $\langle x^2 \rangle$")
a2.plot(t, t, color=C["ink"], lw=0.8, ls="--", label=r"이론: $\langle x^2 \rangle = 2Dt$")
a2.plot(t, x.mean(axis=0), color=C["red"], lw=1.4, label=r"평균 변위 $\langle x \rangle \approx 0$")
a2.set_xlabel("시간 (걸음 수)")
a2.set_ylabel("걸음 크기² 단위")
a2.set_title("걷는 사람 2000명의 평균")
a2.legend(fontsize=8.5, loc="upper left")
a2.set_xlim(0, n)
fig.tight_layout()
save(fig, __file__)
