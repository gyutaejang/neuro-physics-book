from figstyle import plt, np, save, C

# 진행 방향(x) 위에서 전기장(세로)과 자기장(비스듬한 '깊이' 방향)을 간단한 사영으로 그린다.
x = np.linspace(0, 4 * np.pi, 400)
E = np.sin(x)
B = np.sin(x)
dx, dy = 0.45, 0.32  # 깊이 방향의 사영 벡터 (B 방향)

fig, ax = plt.subplots(figsize=(6.8, 3.0))
ax.plot([0, 4 * np.pi + 0.8], [0, 0], color=C["gray"], lw=1)
ax.annotate("", xy=(4 * np.pi + 1.1, 0), xytext=(4 * np.pi + 0.5, 0),
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=1.2))
ax.text(4 * np.pi + 1.2, -0.12, "진행 방향\n(속력 c)", fontsize=8.5, va="top", ha="center", color=C["ink"])
# 전기장
ax.plot(x, E, color=C["blue"], lw=1.8, label="전기장 E")
for xi in np.linspace(0, 4 * np.pi, 33):
    ax.plot([xi, xi], [0, np.sin(xi)], color=C["blue"], lw=0.6, alpha=0.6)
# 자기장 (깊이 방향 사영)
bx = x + B * dx * 1.6
by = B * (-dy) * 1.6
ax.plot(bx, by, color=C["purple"], lw=1.8, label="자기장 B")
for xi in np.linspace(0, 4 * np.pi, 33):
    b = np.sin(xi)
    ax.plot([xi, xi + b * dx * 1.6], [0, -b * dy * 1.6], color=C["purple"], lw=0.6, alpha=0.6)
# 파장 표시
ax.annotate("", xy=(np.pi / 2, 1.3), xytext=(np.pi / 2 + 2 * np.pi, 1.3),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.9))
ax.text(np.pi / 2 + np.pi, 1.38, "파장 λ", ha="center", va="bottom", fontsize=9)
ax.text(np.pi / 2, 1.02, "E", color=C["blue"], fontsize=11, weight="bold", ha="right")
ax.text(np.pi / 2 + 0.85, -0.85, "B", color=C["purple"], fontsize=11, weight="bold")
ax.text(9.2, -1.25, "E와 B는 서로 수직이고\n진행 방향과도 수직이다 (횡파)", fontsize=8.5, color=C["ink"], va="center")
ax.set_xlim(-0.3, 4 * np.pi + 2.0)
ax.set_ylim(-1.55, 1.7)
ax.axis("off")
ax.legend(loc="upper right", fontsize=8.5, bbox_to_anchor=(1.0, 1.05))
save(fig, __file__)
