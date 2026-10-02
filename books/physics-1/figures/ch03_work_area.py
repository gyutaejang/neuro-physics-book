from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9))

# 왼쪽: 일정한 힘
x = np.linspace(0, 3, 50)
a1.fill_between([0.5, 2.5], 0, 4, color=C["red"], alpha=0.15, lw=0)
a1.plot([0, 3], [4, 4], color=C["red"], lw=2)
a1.text(1.5, 2.0, "넓이 = 힘 × 거리\n= 4 N × 2 m = 8 J", ha="center", va="center", fontsize=9)
a1.annotate("", xy=(2.5, 0.4), xytext=(0.5, 0.4),
            arrowprops=dict(arrowstyle="<->", color=C["gray"]))
a1.text(1.5, 0.55, "이동 거리 2 m", ha="center", va="bottom", fontsize=8.5, color=C["gray"])
a1.set_xlim(0, 3)
a1.set_ylim(0, 5.5)
a1.set_title("일정한 힘")
a1.set_xlabel("위치 x (m)")
a1.set_ylabel("힘 F (N)")

# 오른쪽: 용수철처럼 거리에 비례해 커지는 힘
x = np.linspace(0, 0.1, 50)
k = 200
a2.fill_between(x, 0, k * x, color=C["red"], alpha=0.15, lw=0)
a2.plot(x, k * x, color=C["red"], lw=2)
a2.text(0.068, 5.5, "삼각형 넓이\n= ½ × 0.1 m × 20 N\n= 1 J", ha="center", va="center", fontsize=9)
a2.text(0.012, 17, "F = kx\n(k = 200 N/m)", fontsize=8.5, color=C["ink"])
a2.set_xlim(0, 0.105)
a2.set_ylim(0, 22)
a2.set_title("늘어날수록 커지는 힘 (용수철)")
a2.set_xlabel("늘어난 길이 x (m)")
a2.set_ylabel("힘 F (N)")
fig.tight_layout()
save(fig, __file__)
