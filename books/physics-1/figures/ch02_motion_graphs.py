from figstyle import plt, np, save, C

# 0–4 s: 가속 2 m/s², 4–8 s: 등속 8 m/s, 8–10 s: 감속 −4 m/s²
t = np.linspace(0, 10, 501)
a = np.where(t < 4, 2.0, np.where(t < 8, 0.0, -4.0))
v = np.where(t < 4, 2 * t, np.where(t < 8, 8.0, 8 - 4 * (t - 8)))
x = np.where(t < 4, t ** 2, np.where(t < 8, 16 + 8 * (t - 4), 48 + 8 * (t - 8) - 2 * (t - 8) ** 2))

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.5, 2.7))

ax1.plot(t, x, color=C["blue"])
tt = np.linspace(0.6, 3.4, 10)
ax1.plot(tt, 4 * (tt - 2) + 4, color=C["red"], lw=1.2)
ax1.scatter([2], [4], color=C["red"], s=14, zorder=3)
ax1.annotate("접선의 기울기\n= 그 순간의 속도\n(t = 2 s에서 4 m/s)", xy=(2.9, 7.6), xytext=(0.2, 40),
             fontsize=8, arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax1.set_title("위치 x")
ax1.set_xlabel("시간 (s)")
ax1.set_ylabel("m")
ax1.set_ylim(0, 62)

ax2.plot(t, v, color=C["blue"])
ax2.fill_between(t, 0, v, color=C["blue"], alpha=0.15)
ax2.text(5, 3.5, "넓이 = 이동 거리\n(56 m)", ha="center", fontsize=8)
ax2.set_title("속도 v")
ax2.set_xlabel("시간 (s)")
ax2.set_ylabel("m/s")
ax2.set_ylim(0, 10.5)

ax3.plot(t, a, color=C["red"], drawstyle="steps-post")
ax3.axhline(0, color=C["gray"], lw=0.6)
ax3.text(2, 2.4, "가속", ha="center", fontsize=8)
ax3.text(6, 0.4, "등속 (a = 0)", ha="center", fontsize=8)
ax3.text(9, -3.4, "감속", ha="center", fontsize=8)
ax3.set_title("가속도 a")
ax3.set_xlabel("시간 (s)")
ax3.set_ylabel("m/s²")
ax3.set_ylim(-5, 3.5)

fig.tight_layout()
save(fig, __file__)
