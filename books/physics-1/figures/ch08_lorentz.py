from figstyle import plt, np, save, C
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


def arrow(ax, p0, p1, col, lw=1.8, ms=14):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw, zorder=5))


def crosses(ax, xs, ys):
    for x in xs:
        for y in ys:
            ax.plot(x, y, marker="x", ms=5, mew=1.0, color=C["purple"], alpha=0.6, zorder=1)


BOX = dict(fc="white", ec="none", pad=1.2)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4))
grid = np.arange(-1.8, 1.81, 0.6)

# (가) 양전하가 종이로 들어가는 자기장 속을 움직인다
crosses(ax1, grid, grid)
R = 1.0
ax1.add_patch(Circle((0, 0), R, fill=False, ls="--", lw=1.0, color=C["gray"], zorder=2))
q = (0, -R)
ax1.add_patch(Circle(q, 0.13, color=C["blue"], zorder=6))
ax1.text(q[0], q[1], "+", color="white", ha="center", va="center", fontsize=10, zorder=7)
arrow(ax1, (0.15, -R), (0.95, -R), C["blue"])
ax1.text(0.6, -R - 0.18, "속도 v", color=C["blue"], fontsize=9, va="top", bbox=BOX, zorder=6)
arrow(ax1, (0, -R + 0.15), (0, -R + 0.85), C["red"])
ax1.text(0.08, -R + 0.62, "힘 F", color=C["red"], fontsize=9, bbox=BOX, zorder=6)
ax1.text(0, 0.12, "원 궤도\n반지름 r = mv / qB", ha="center", va="center", fontsize=8.5, color=C["gray"], bbox=BOX, zorder=6)
ax1.text(0, 2.2, "자기장 B: 종이로 들어감 (×)", ha="center", fontsize=8.5, color=C["purple"], bbox=BOX, zorder=6)
ax1.set_title("(가) 움직이는 전하: F = qvB", fontsize=10.5, pad=14)

# (나) 전류가 흐르는 도선
crosses(ax2, grid, grid)
ax2.add_patch(Rectangle((-0.06, -1.9), 0.12, 3.8, color=C["ink"], zorder=3))
arrow(ax2, (0.25, -0.9), (0.25, 0.3), C["blue"])
ax2.text(0.35, -0.3, "전류 I", color=C["blue"], fontsize=9, bbox=BOX, zorder=6)
arrow(ax2, (-0.12, 0.9), (-1.1, 0.9), C["red"])
ax2.text(-1.1, 1.05, "힘 F = ILB", color=C["red"], fontsize=9, ha="left", bbox=BOX, zorder=6)
ax2.text(0, 2.2, "자기장 B: 종이로 들어감 (×)", ha="center", fontsize=8.5, color=C["purple"], bbox=BOX, zorder=6)
ax2.set_title("(나) 전류가 흐르는 도선: F = ILB", fontsize=10.5, pad=14)

for ax in (ax1, ax2):
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.1, 2.4)
    ax.set_aspect("equal")
    ax.axis("off")
save(fig, __file__)
