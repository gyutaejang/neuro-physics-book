from figstyle import plt, np, save, C

rng = np.random.default_rng(7)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9))
n_walk, n_step, s = 400, 1500, 0.1


def walks(wall=None):
    p = np.zeros((n_walk, n_step + 1, 2))
    for i in range(n_step):
        q = p[:, i] + rng.normal(0, s, (n_walk, 2))
        if wall is not None:  # 벽을 넘으면 거울처럼 튕겨 돌아온다
            over = np.abs(q[:, 1]) > wall
            q[over, 1] = np.sign(q[over, 1]) * 2 * wall - q[over, 1]
        p[:, i + 1] = q
    return p


for ax, wall, title in [(a1, None, "자유 확산: 모든 방향이 같다 (등방성)"),
                        (a2, 1.5, "축삭 안: 가로로 막힌다 (비등방성)")]:
    p = walks(wall)
    ax.scatter(p[:, -1, 0], p[:, -1, 1], s=3, color=C["blue"], alpha=0.5, lw=0)
    ax.plot(p[0, :, 0], p[0, :, 1], color=C["red"], lw=0.5)
    if wall:
        for sg in (-1, 1):
            ax.axhline(sg * wall, color=C["ink"], lw=2.2)
        ax.text(0, 2.0, "세포막과 수초 (벽)", ha="center", fontsize=8.5)
        ax.annotate("", xy=(9, -3.6), xytext=(-9, -3.6),
                    arrowprops=dict(arrowstyle="<->", color=C["purple"], lw=1.2))
        ax.text(0, -4.3, "섬유 방향으로만 멀리 퍼진다", ha="center", va="top", fontsize=8.5, color=C["purple"])
    ax.set_xlim(-12, 12)
    ax.set_ylim(-11, 11)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(title, fontsize=10)
    ax.scatter([0], [0], color=C["ink"], marker="x", s=25, zorder=4)
fig.tight_layout()
save(fig, __file__)
