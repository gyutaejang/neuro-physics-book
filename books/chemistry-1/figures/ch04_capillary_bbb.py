from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch, Circle

fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.3))
rng = np.random.default_rng(5)


def panel(ax, tight, title):
    # 내피세포 띠
    xs = [0.0, 2.1, 4.2]
    for x0 in xs:
        w = 2.1 if tight else 1.8
        ax.add_patch(FancyBboxPatch((x0 + (0 if tight else 0.15), 1.4), w - 0.02, 0.6,
                                    boxstyle="round,pad=0.02", fc="#f3e3d3", ec=C["red"], lw=0.8))
    if tight:
        for xj in (2.1, 4.2):
            ax.plot([xj, xj], [1.38, 2.02], color=C["ink"], lw=3)
    # 혈장 쪽 입자
    for _ in range(9):
        ax.scatter(rng.uniform(0.2, 6.1), rng.uniform(2.35, 3.2), s=14, color=C["green"], zorder=3)
    for x in (0.9, 3.0, 5.2):
        ax.add_patch(Circle((x, 2.75), 0.17, fc=C["red"], ec="none", alpha=0.8, zorder=3))
    # 조직 쪽 입자
    for _ in range(9):
        ax.scatter(rng.uniform(0.2, 6.1), rng.uniform(0.25, 1.05), s=14, color=C["green"], zorder=3)
    ax.text(0.05, 3.45, "혈관 안 (혈장)", fontsize=8.5)
    ax.text(0.05, -0.05, "뇌 조직 (세포 사이 공간)" if tight else "조직 (세포 사이 공간)", fontsize=8.5, va="top")
    if tight:
        for xg in (2.1, 4.2):
            ax.annotate("", xy=(xg, 2.05), xytext=(xg, 2.5),
                        arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.2, mutation_scale=9))
            ax.text(xg + 0.08, 2.3, "×", color=C["red"], fontsize=13, va="center")
        ax.annotate("", xy=(1.05, 1.1), xytext=(1.05, 2.35),
                    arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.8, mutation_scale=12))
        ax.text(1.18, 1.7, "물", color=C["blue"], fontsize=9, va="center",
                bbox=dict(fc="#f3e3d3", ec="none", pad=0.5))
        ax.text(3.15, -0.55, "치밀 이음부가 Na⁺, Cl⁻까지 막는다\n→ 1 mOsm/L 차이도 약 19 mmHg로 물을 민다",
                ha="center", va="top", fontsize=8, color=C["ink"])
    else:
        for xg in (2.05, 4.15):
            ax.annotate("", xy=(xg, 1.1), xytext=(xg, 2.4),
                        arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.2, mutation_scale=9))
        ax.annotate("", xy=(3.0, 2.08), xytext=(3.0, 2.55),
                    arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.2, mutation_scale=9))
        ax.text(3.08, 2.3, "×", color=C["red"], fontsize=13, va="center")
        ax.text(3.15, -0.55, "작은 이온은 틈으로 자유롭게 지난다\n→ 물을 붙잡는 것은 단백질뿐 (약 25 mmHg)",
                ha="center", va="top", fontsize=8, color=C["ink"])
    ax.set_title(title, fontsize=10)
    ax.set_xlim(-0.1, 6.4)
    ax.set_ylim(-1.5, 3.7)
    ax.axis("off")


panel(axes[0], False, "말초 모세혈관")
panel(axes[1], True, "뇌 모세혈관 (혈액뇌장벽)")
axes[0].scatter([0.4], [-1.35], s=14, color=C["green"])
axes[0].text(0.55, -1.35, "작은 이온 (Na⁺, Cl⁻)", fontsize=7.5, va="center")
axes[0].add_patch(Circle((3.6, -1.35), 0.12, fc=C["red"], alpha=0.8, ec="none"))
axes[0].text(3.8, -1.35, "단백질 (알부민)", fontsize=7.5, va="center")
fig.tight_layout()
save(fig, __file__)
