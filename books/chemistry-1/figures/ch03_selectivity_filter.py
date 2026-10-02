from figstyle import plt, np, save, C

fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[1, 1, 1]))
O_R = 0.14  # 산소 원자 반지름 (도식용, nm 비례)

def oxygen(ax, x, y, col=C["red"]):
    ax.add_patch(plt.Circle((x, y), 0.07, facecolor=col, edgecolor=C["ink"], lw=0.6, zorder=3))

def cation(ax, x, y, r, label, col=C["green"]):
    ax.add_patch(plt.Circle((x, y), r, facecolor=col, alpha=0.85, edgecolor=C["ink"], lw=0.8, zorder=4))
    ax.text(x, y, label, ha="center", va="center", fontsize=8.5, color="white", zorder=5)

# (가) 물속의 K⁺: 물 산소가 둘러싼다
a = axes[0]
cation(a, 0, 0, 0.10, "K⁺")
for k in range(8):
    t = 2 * np.pi * k / 8 + 0.2
    cx, cy = 0.28 * np.cos(t), 0.28 * np.sin(t)
    for s in (+1, -1):
        h = t + s * np.deg2rad(52)
        hx, hy = cx + 0.1 * np.cos(h), cy + 0.1 * np.sin(h)
        a.plot([cx, hx], [cy, hy], color=C["ink"], lw=0.9, zorder=2)
        a.add_patch(plt.Circle((hx, hy), 0.035, facecolor="white", edgecolor=C["ink"], lw=0.5, zorder=3))
    oxygen(a, cx, cy, C["blue"])
a.text(0, -1.05, "(가) 물속 K⁺\n물 분자 산소 6–8개가 둘러싼다", ha="center", va="top", fontsize=8.5)

# (나) 선택성 필터: 마주 보는 두 서브유닛의 카보닐 산소 줄 (실제로는 네 개가 둘러싼다)
a = axes[1]
zs = np.linspace(-0.6, 0.6, 5)  # 산소 고리 5층, 간격 약 0.3 nm
for side in (-1, 1):
    x_wall = side * 0.28
    a.add_patch(plt.Rectangle((x_wall + (0 if side > 0 else -0.16), -0.75), 0.16, 1.5,
                              color=C["gray"], alpha=0.25, lw=0, zorder=1))
    for z in zs:
        a.plot([x_wall, x_wall + side * 0.08], [z, z], color=C["ink"], lw=1.4, zorder=2)
        oxygen(a, x_wall - side * 0.07, z)
sites = (zs[:-1] + zs[1:]) / 2
for i, z in enumerate(sites):
    a.text(0.5, z, f"S{4 - i}", fontsize=8, va="center", color=C["gray"])
    if i % 2 == 0:
        cation(a, 0, z, 0.10, "K⁺")
    else:
        oxygen(a, 0, z, C["blue"])
a.text(0, 0.86, "세포 밖", ha="center", fontsize=8.5)
a.text(0, -0.8, "세포 안쪽", ha="center", va="top", fontsize=8.5)
a.text(0, -1.05, "(나) K⁺ 통로 선택성 필터\n카보닐 산소 8개가 물 껍질을 대신한다", ha="center", va="top", fontsize=8.5)

# (다) Na⁺는 너무 작아 네 방향의 산소에 동시에 닿지 못한다
a = axes[2]
for t in np.deg2rad([45, 135, 225, 315]):
    x, y = 0.25 * np.cos(t), 0.25 * np.sin(t)
    oxygen(a, x, y)
    a.plot([0.07 * np.cos(t), x - 0.07 * np.cos(t)], [0.07 * np.sin(t), y - 0.07 * np.sin(t)],
           color=C["red"], lw=0.8, ls=":")
cation(a, 0, 0, 0.077, "Na⁺")
a.text(0, -1.05, "(다) 필터 속 Na⁺\n산소와의 거리가 맞지 않아\n잃은 물 껍질을 보상받지 못한다",
       ha="center", va="top", fontsize=8.5)
for a in axes:
    a.set_xlim(-0.62, 0.62)
    a.set_ylim(-1.55, 1.0)
    a.set_aspect("equal")
    a.axis("off")
fig.tight_layout()
save(fig, __file__)
