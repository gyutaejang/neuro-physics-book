from figstyle import plt, np, save, C
from matplotlib.patches import Circle, Rectangle

fig, axes = plt.subplots(1, 3, figsize=(7.3, 3.1))
specs = [
    ("정상", 0.36, 1.0, False, "세포 사이 공간 약 20%"),
    ("세포독성 부종", 0.46, 1.0, False, "세포가 붓고 사이 공간이 좁아진다\nADC 감소 (DWI 밝음)"),
    ("혈관성 부종", 0.36, 1.22, True, "혈액뇌장벽이 새어 사이 공간에\n단백질과 물이 고인다 · ADC 증가"),
]
for ax, (title, r, sp, leak, note) in zip(axes, specs):
    # 모세혈관 (위)
    ax.add_patch(Rectangle((-0.1, 3.35), 3.2, 0.35, fc="#f3e3d3", ec=C["red"], lw=0.8))
    ax.text(1.5, 3.85, "모세혈관", ha="center", fontsize=8, color=C["red"])
    if leak:
        ax.add_patch(Rectangle((1.35, 3.33), 0.3, 0.4, fc="white", ec="none"))
        for dx in (-0.25, 0.0, 0.25):
            ax.annotate("", xy=(1.5 + dx * 2.4, 3.05), xytext=(1.5, 3.4),
                        arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.1, mutation_scale=8))
    # 조직: 세포 격자
    tissue_fc = "#cfe0f1" if leak else C["light"]
    ax.add_patch(Rectangle((-0.1, -0.1), 3.2, 3.3, fc=tissue_fc, ec="none"))
    n = 3
    step = 0.95 * sp
    off = 1.5 - step * (n - 1) / 2
    for i in range(n):
        for j in range(n):
            ax.add_patch(Circle((off + i * step, 1.55 - step + j * step), r,
                                fc="#dcebd8", ec=C["green"], lw=1.3))
    ax.set_title(title, fontsize=10)
    ax.text(1.5, -0.3, note, ha="center", va="top", fontsize=7.8)
    ax.set_xlim(-0.2, 3.2)
    ax.set_ylim(-1.2, 4.1)
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout(w_pad=0.6)
save(fig, __file__)
