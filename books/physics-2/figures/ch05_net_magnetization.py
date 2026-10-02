from figstyle import plt, np, save, C

# 스핀 N개의 방향을 무작위로 뽑는다. (나)는 B₀ 쪽으로 치우친 분포 p(θ) ∝ 1 + ε cos θ.
# 실제 치우침(3 T, 37 °C)은 ε ≈ 3 × 10⁻⁵ 정도이므로 그림은 크게 과장했다.
rng = np.random.default_rng(5)
N = 120


def sample(eps):
    out = []
    while len(out) < N:
        v = rng.normal(size=3)
        v /= np.linalg.norm(v)
        if rng.uniform() < (1 + eps * v[2]) / (1 + eps):
            out.append(v)
    return np.array(out)


fig = plt.figure(figsize=(7.0, 3.0))
for i, (eps, title) in enumerate([(0.0, "(가) 자기장이 없을 때"), (0.9, "(나) B₀ 안에서 (치우침 과장)")]):
    ax = fig.add_subplot(1, 2, i + 1, projection="3d", computed_zorder=False)
    v = sample(eps)
    up = v[:, 2] >= 0
    for sel, col in [(up, C["purple"]), (~up, C["gray"])]:
        ax.quiver(0, 0, 0, v[sel, 0], v[sel, 1], v[sel, 2], color=col, lw=0.5,
                  arrow_length_ratio=0.12, alpha=0.4)
    M = v.mean(axis=0)
    s = 3.4  # 합 벡터를 보기 좋게 늘림
    if i == 1:
        ax.quiver(0, 0, 0, s * M[0], s * M[1], s * M[2], color=C["red"], lw=2.6, arrow_length_ratio=0.35, zorder=10)
        ax.text(s * M[0] + 0.3, s * M[1] + 0.3, s * M[2] - 0.15, "M (합)", color=C["red"], fontsize=10.5, zorder=11,
                bbox=dict(fc="white", ec="none", pad=1, alpha=0.85))
    else:
        ax.scatter([0], [0], [0], color=C["red"], s=30, zorder=10)
        ax.text(0.15, 0, -0.25, "M ≈ 0", color=C["red"], fontsize=10.5, zorder=11,
                bbox=dict(fc="white", ec="none", pad=1, alpha=0.85))
    if i == 1:
        ax.quiver(1.0, 1.0, -0.6, 0, 0, 0.9, color=C["purple"], lw=1.5, arrow_length_ratio=0.2)
        ax.text(1.0, 1.0, 0.4, "B₀", color=C["purple"], fontsize=10)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=14, azim=-60)
    ax.set_axis_off()
    ax.set_title(title, fontsize=10.5, y=0.95)
    ax.text2D(0.5, 0.06, f"위쪽 반구 {up.sum()}개, 아래쪽 {(~up).sum()}개", transform=ax.transAxes,
              ha="center", fontsize=8.5)
fig.subplots_adjust(left=0, right=1, bottom=0.02, top=0.95, wspace=0)
save(fig, __file__)
