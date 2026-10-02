from figstyle import plt, np, save, C

# 이상적인 이상성(biphasic) TMS 펄스: 코일 전류가 사인파 한 주기 동안 흐른다.
T = 300e-6           # 한 주기 약 300 μs
B0 = 1.0             # 피질 위치의 최대 자기장 (T), 어림값
t = np.linspace(-40e-6, 380e-6, 2000)
on = (t >= 0) & (t <= T)
B = np.where(on, B0 * np.sin(2 * np.pi * t / T), 0.0)
dBdt = np.where(on, B0 * 2 * np.pi / T * np.cos(2 * np.pi * t / T), 0.0)

fig, ax1 = plt.subplots(figsize=(6.4, 3.0))
us = t * 1e6
ax1.plot(us, B, color=C["purple"], label="코일 자기장 B (왼쪽 축)")
ax1.set_ylabel("자기장 B (T)", color=C["purple"])
ax1.set_ylim(-1.5, 1.5)
ax1.set_xlabel("시간 (μs)")
ax1.axhline(0, color=C["gray"], lw=0.6)
ax2 = ax1.twinx()
ax2.spines["right"].set_visible(True)
ax2.plot(us, dBdt / 1e4, color=C["blue"], ls="--", label="dB/dt ∝ 유도 전기장 (오른쪽 축)")
ax2.set_ylabel("dB/dt (×10⁴ T/s)", color=C["blue"])
ax2.set_ylim(-3.2, 3.2)
ax1.set_xlim(-40, 380)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="lower left", fontsize=8)
ax1.annotate("B 최대 → dB/dt = 0", xy=(75, 1.0), xytext=(5, 1.22), fontsize=8.5,
             arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax1.annotate("B = 0 → dB/dt 최대", xy=(150, 0), xytext=(165, 1.22), fontsize=8.5,
             arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
save(fig, __file__)
