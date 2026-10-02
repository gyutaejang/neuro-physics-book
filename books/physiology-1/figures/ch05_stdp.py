from figstyle import plt, np, save, C

# 그림용 어림값: 앞섬 쪽 진폭 0.8, 시간 상수 17 ms; 뒤짐 쪽 진폭 0.4, 시간 상수 34 ms
Ap, tp, Am, tm = 80, 17, 40, 34
rng = np.random.default_rng(5)
dt_pos = rng.uniform(2, 100, 26)
dt_neg = -rng.uniform(2, 100, 26)
pts_pos = Ap * np.exp(-dt_pos / tp) + rng.normal(0, 12, dt_pos.size)
pts_neg = -Am * np.exp(dt_neg / tm) + rng.normal(0, 9, dt_neg.size)

fig, ax = plt.subplots(figsize=(6.4, 3.0))
ax.axhline(0, color=C["gray"], lw=0.7)
ax.axvline(0, color=C["gray"], lw=0.7)
ax.scatter(dt_pos, pts_pos, s=12, color=C["red"], alpha=0.55, lw=0)
ax.scatter(dt_neg, pts_neg, s=12, color=C["blue"], alpha=0.55, lw=0)
x1 = np.linspace(0.5, 100, 200)
x2 = np.linspace(-100, -0.5, 200)
ax.plot(x1, Ap * np.exp(-x1 / tp), color=C["red"], lw=1.8)
ax.plot(x2, -Am * np.exp(x2 / tm), color=C["blue"], lw=1.8)
ax.text(30, 62, "앞 → 뒤 (Δt > 0)\n강화(LTP)", fontsize=8.5, color=C["red"])
ax.text(-95, -66, "뒤 → 앞 (Δt < 0)\n약화(LTD)", fontsize=8.5, color=C["blue"])
ax.text(52, -38, "시간 상수 약 17 ms (강화)\n약 34 ms (약화)", fontsize=8, color=C["gray"])
ax.set_xlabel("Δt = 시냅스 뒤 스파이크 시각 − 시냅스 앞 스파이크 시각 (ms)")
ax.set_ylabel("시냅스 세기 변화 (%)")
ax.set_xlim(-105, 105)
ax.set_ylim(-80, 110)
fig.tight_layout()
save(fig, __file__)
