from figstyle import plt, np, save, C

# (가) 블록 설계 시계열: 데이터 y = β0·상수 + β1·과제 + 잔차
# (나) 관측 3개짜리 장난감 예에서 본 기하: 최소제곱 적합은 y를 설계 행렬의 열이 펼치는 평면에 수직으로 내린 그림자다.
rng = np.random.default_rng(2)
t = np.arange(80)
task = ((t // 10) % 2 == 1).astype(float)
k = np.exp(-np.arange(12) / 2.5)
task = np.convolve(task, k / k.sum())[:80]
y = 100 + 1.0 * task + rng.normal(0, 0.45, 80)
X = np.c_[np.ones(80), task]
b, *_ = np.linalg.lstsq(X, y, rcond=None)
fit = X @ b

fig = plt.figure(figsize=(7.4, 3.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.1])
ax1 = fig.add_subplot(gs[0])
ax1.plot(t, y, "o", ms=2.6, color=C["blue"], label="데이터 y")
ax1.plot(t, fit, color=C["red"], lw=1.5, label=f"적합 Xβ ($\\beta_1$ = {b[1]:.2f})")
for i in range(0, 80, 1):
    ax1.plot([t[i], t[i]], [fit[i], y[i]], color=C["gray"], lw=0.4)
ax1.set_xlabel("스캔 번호")
ax1.set_ylabel("신호 (임의 단위)")
ax1.set_title("(가) 적합과 잔차(회색 선)", fontsize=9.5)
ax1.legend(fontsize=7.5, loc="upper left", ncol=1)
ax1.set_ylim(98.6, 102.6)

ax = fig.add_subplot(gs[1])
# 평면을 비스듬히 본 2차원 도식. 평면 좌표 (a, b) → 그림 좌표 a·u + b·v
u = np.array([1.0, 0.0])
v = np.array([0.6, 0.55])
O = np.array([0.0, 0.0])


def P(a, b):
    return O + a * u + b * v


corners = np.array([P(-0.2, -0.55), P(2.8, -0.55), P(2.8, 1.9), P(-0.2, 1.9)])
ax.fill(corners[:, 0], corners[:, 1], color="#dbe5f1", ec=C["gray"], lw=0.6, zorder=0)
kw = dict(arrowstyle="-|>", mutation_scale=12)
x1e, x2e = P(1.4, 0), P(0.1, 1.3)
yh = P(1.7, 0.9)
yv = yh + np.array([0, 1.5])
ax.annotate("", xy=x1e, xytext=O, arrowprops=dict(color=C["gray"], lw=1.5, **kw))
ax.annotate("", xy=x2e, xytext=O, arrowprops=dict(color=C["gray"], lw=1.5, **kw))
ax.annotate("", xy=yv, xytext=O, arrowprops=dict(color=C["blue"], lw=1.9, **kw))
ax.annotate("", xy=yh, xytext=O, arrowprops=dict(color=C["red"], lw=1.9, **kw))
ax.plot([yh[0], yv[0]], [yh[1], yv[1]], color=C["ink"], lw=1.0, ls="--")
# 직각 표시
q = 0.12
c1 = yh + np.array([0, q])
c2 = c1 - q * u / np.linalg.norm(u) * 1.2
c3 = yh - q * u * 1.2
ax.plot([c1[0], c2[0], c3[0]], [c1[1], c2[1], c3[1]], color=C["ink"], lw=0.7)
ax.text(*(x1e + [0.0, -0.06]), "$x_1$ 상수", fontsize=8.5, color=C["ink"], ha="center", va="top")
ax.text(*(x2e + [-0.1, 0.06]), "$x_2$ 과제", fontsize=8.5, color=C["ink"], ha="right")
ax.text(*(yv + [-0.08, 0.02]), "y 데이터", fontsize=8.5, color=C["blue"], ha="right")
ax.text(*(yh + [0.1, -0.22]), "ŷ = Xβ (적합)", fontsize=8.5, color=C["red"])
ax.text(yh[0] + 0.1, yh[1] + 1.05, "잔차 e\n(평면에 수직)", fontsize=8, color=C["ink"], va="center")
ax.set_xlim(-0.3, 4.0)
ax.set_ylim(-0.45, 3.0)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("(나) 적합은 회귀자 평면 위로의 투영", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
