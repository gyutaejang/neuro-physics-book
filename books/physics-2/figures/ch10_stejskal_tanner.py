from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle

# 스테이스칼-태너 펄스 경사 스핀 에코: G = 40 mT/m, δ = 20 ms, Δ = 30 ms, TE = 60 ms
gam = 2.675e8
G, d, D, TE = 0.040, 20e-3, 30e-3, 60e-3
t1 = 5e-3
dt = 1e-5
t = np.arange(0, 66e-3, dt)
g_eff = np.zeros_like(t)          # 180° 펄스의 위상 반전을 포함한 '유효' 경사
g_eff[(t >= t1) & (t < t1 + d)] = G
g_eff[(t >= t1 + D) & (t < t1 + D + d)] = -G
g_real = np.abs(g_eff)            # 실제로 거는 경사: 두 엽 모두 같은 극성

fig = plt.figure(figsize=(7.2, 4.4))
gs = fig.add_gridspec(3, 1, height_ratios=[0.55, 0.75, 1.7], hspace=0.12)
ax0 = fig.add_subplot(gs[0])
ax1 = fig.add_subplot(gs[1], sharex=ax0)
ax2 = fig.add_subplot(gs[2], sharex=ax0)
ms = t * 1e3

# RF와 신호
ax0.axhline(0, color=C["gray"], lw=0.6)
for tc, h, lab in [(0.5, 0.6, "90°"), (TE / 2 * 1e3, 1.0, "180°")]:
    ax0.add_patch(Rectangle((tc - 0.6, 0), 1.2, h, color=C["purple"]))
    ax0.text(tc + 1.2, h * 0.75, lab, fontsize=8.5, color=C["purple"], va="center")
ts = np.linspace(56, 64, 300)
ax0.plot(ts, 0.55 * np.sinc((ts - 60) / 1.2) * np.cos((ts - 60) * 6), color=C["blue"], lw=1)
ax0.text(60, 0.75, "에코 (TE 60 ms)", fontsize=8, color=C["blue"], ha="center")
ax0.set_ylim(-0.6, 1.25)
ax0.set_yticks([])
ax0.set_ylabel("RF", rotation=0, ha="right", va="center")

# 확산 경사
ax1.fill_between(ms, 0, g_real * 1e3, color=C["red"], alpha=0.3, step="pre")
ax1.plot(ms, g_real * 1e3, color=C["red"], lw=1.4, drawstyle="steps-pre")
ax1.set_ylim(0, 58)
ax1.set_yticks([0, 40])
ax1.set_ylabel("G (mT/m)")
ax1.annotate("", xy=(t1 * 1e3, 47), xytext=((t1 + d) * 1e3, 47),
             arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.7))
ax1.text((t1 + d / 2) * 1e3, 50, "δ = 20 ms", ha="center", fontsize=8)
ax1.annotate("", xy=(t1 * 1e3, 30), xytext=((t1 + D) * 1e3, 30),
             arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.7))
ax1.text((t1 + D) * 1e3 - 5, 21, "Δ = 30 ms", fontsize=8, color=C["gray"], ha="center")
ax1.axvline((t1 + D) * 1e3, ymax=0.85, color=C["gray"], lw=0.5, ls=":")
ax1.text(67, 26, "두 엽은 같은 극성.\n180°가 그 사이 위상을\n뒤집어 둘째 엽이\n첫째 엽을 되감는다.",
         fontsize=7.5, color=C["ink"], va="center")
ax2.set_xticks([0, 10, 20, 30, 40, 50, 60])

# 스핀 위상: 정지한 물(점선)과 확산하는 물(실선)
rng = np.random.default_rng(3)
Dw = 1.0e-9                       # 조직 물의 확산계수 1.0×10⁻³ mm²/s = 1.0×10⁻⁹ m²/s
n = 9
x0 = np.linspace(-12e-6, 12e-6, n)
steps = rng.normal(0, np.sqrt(2 * Dw * dt), (n, len(t)))
x = x0[:, None] + np.cumsum(steps, axis=1)
phase_move = gam * np.cumsum(g_eff[None, :] * x, axis=1) * dt
phase_still = gam * np.cumsum(g_eff[None, :] * x0[:, None] * np.ones_like(t), axis=1) * dt
for k in range(n):
    ax2.plot(ms, phase_still[k], color=C["gray"], lw=0.7, ls="--")
    ax2.plot(ms, phase_move[k], color=C["blue"], lw=1.1)
end = phase_move[:, np.searchsorted(t, TE)]
ax2.axhline(0, color=C["gray"], lw=0.6)
ax2.text(67, 1.3, "정지한 물(회색 점선):\n모두 0으로 돌아온다", fontsize=7.5, color=C["gray"], va="center")
ax2.text(1, 3.6, "위치에 비례해 위상이 쌓인다 (x = −12 … +12 μm)", fontsize=8, ha="left")
ax2.text(67, -1.4, "확산한 물(파랑):\n남은 위상이 제각각\n→ 더하면 신호가 준다", fontsize=8, color=C["blue"])
ax2.set_ylabel("위상 (rad)")
ax2.set_xlabel("90° 펄스 뒤 시간 (ms)")
ax2.set_xlim(-1, 88)
ax2.set_ylim(-3.4, 4.1)
for a in (ax0, ax1):
    plt.setp(a.get_xticklabels(), visible=False)
    a.spines["bottom"].set_visible(False)
    a.tick_params(axis="x", length=0)
save(fig, __file__)
