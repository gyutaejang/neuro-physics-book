from figstyle import plt, np, save, C

# 4 × 4 복셀의 자화 방향(위상). (가) 들뜸 직후 (나) 위상 부호화 경사 Gy 뒤 (다) 읽기 경사 Gx를 켠 채 시간이 흐른 뒤.
n = 4
xs, ys = np.meshgrid(np.arange(n), np.arange(n))
cases = [
    (np.zeros((n, n)), "(가) 들뜸 직후", "모두 같은 위상"),
    (2 * np.pi * ys / n * 0.75, "(나) 위상 부호화 $G_y$ 뒤", "줄(y)마다 위상이 다르다"),
    (2 * np.pi * ys / n * 0.75 + 2 * np.pi * xs / n * 0.6, "(다) 읽기 $G_x$ 동안", "열(x)마다 도는 빠르기가 다르다"),
]
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.9))
for ax, (ph, title, sub) in zip(axs, cases):
    for i in range(n):
        for j in range(n):
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fc=C["light"], ec="white", lw=1.5))
            ax.add_patch(plt.Circle((j, i), 0.38, fill=False, color=C["gray"], lw=0.6))
            p = ph[i, j]
            ax.annotate("", xy=(j + 0.34 * np.sin(p), i + 0.34 * np.cos(p)), xytext=(j, i),
                        arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.4, mutation_scale=9,
                                        shrinkA=0, shrinkB=0))
    ax.set_xlim(-0.7, n - 0.3)
    ax.set_ylim(-1.3, n - 0.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    ax.text((n - 1) / 2, -1.0, sub, ha="center", fontsize=8.5)
# 방향 표시
axs[1].annotate("", xy=(-0.62, 3.3), xytext=(-0.62, -0.4), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1))
axs[1].text(-0.62, 3.45, "y", color=C["red"], ha="center", fontsize=9)
axs[2].annotate("", xy=(3.4, -0.62), xytext=(-0.4, -0.62), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1))
axs[2].text(3.55, -0.62, "x", color=C["red"], va="center", fontsize=9)
fig.tight_layout()
save(fig, __file__)
