from figstyle import plt, np, save, C
from matplotlib.patches import Ellipse, Circle, Polygon, FancyBboxPatch, Rectangle

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.4), gridspec_kw=dict(width_ratios=[1.55, 1]))

# ---- 왼쪽: 세포체 도식 ----
ax = a1
# 세포체 윤곽 (돌기 시작부 포함)
th = np.linspace(0, 2 * np.pi, 400)
r = 1.0 + 0.06 * np.sin(3 * th)
x, y = 1.55 * r * np.cos(th), 1.15 * r * np.sin(th)
ax.fill(x, y, fc="#eef5ec", ec=C["green"], lw=1.6, zorder=1)
# 축삭 둔덕 쪽 돌기와 수상돌기 줄기
ax.add_patch(Polygon([(1.45, 0.25), (2.6, 0.08), (2.6, -0.08), (1.45, -0.25)], fc="#eef5ec", ec=C["green"], lw=1.4, zorder=0))
ax.add_patch(Polygon([(-1.4, 0.35), (-2.5, 0.75), (-2.55, 0.6), (-1.45, 0.1)], fc="#eef5ec", ec=C["green"], lw=1.4, zorder=0))
ax.add_patch(Polygon([(-1.3, -0.45), (-2.4, -0.95), (-2.35, -1.08), (-1.2, -0.65)], fc="#eef5ec", ec=C["green"], lw=1.4, zorder=0))
# 핵과 인
ax.add_patch(Circle((-0.25, 0.05), 0.55, fc="#dbe6f3", ec=C["blue"], lw=1.3, zorder=2))
ax.add_patch(Circle((-0.15, 0.12), 0.15, fc=C["blue"], ec="none", alpha=0.7, zorder=3))
# 거친면 소포체 (니슬 소체): 곡선 + 리보솜 점
for k, (cx, cy, ang) in enumerate([(-0.65, 0.78, 10), (0.55, 0.72, -15), (-0.9, -0.72, -10)]):
    for j in range(3):
        t = np.linspace(-0.35, 0.35, 30)
        xx = cx + t * np.cos(np.radians(ang)) - (0.09 * j) * np.sin(np.radians(ang))
        yy = cy + t * np.sin(np.radians(ang)) + (0.09 * j) * np.cos(np.radians(ang)) + 0.04 * np.cos(t * 6)
        ax.plot(xx, yy, color=C["purple"], lw=1.0, zorder=3)
        ax.scatter(xx[::4], yy[::4], s=2.5, color=C["purple"], zorder=4)
# 골지체: 겹친 활 모양
for j in range(4):
    t = np.linspace(-0.3 + 0.03 * j, 0.3 - 0.03 * j, 30)
    ax.plot(0.65 + t, -0.35 - 0.07 * j + 0.5 * t ** 2, color=C["red"], lw=1.6, zorder=3)
# 미토콘드리아
for (mx, my, ang) in [(0.95, 0.15, 20), (0.35, -0.85, -10), (-1.05, 0.15, 75), (2.1, 0.0, 0)]:
    w = 0.42 if mx < 2 else 0.3
    ax.add_patch(Ellipse((mx, my), w, 0.16 if mx < 2 else 0.1, angle=ang, fc="#f6dcc8", ec=C["red"], lw=1.0, zorder=3))
# 미세소관 (돌기 안으로)
for dy in (-0.04, 0.04):
    ax.plot([1.3, 2.55], [dy * 1.5, dy], color=C["gray"], lw=0.7, zorder=2)
for dy in (-0.05, 0.05):
    ax.plot([-1.3, -2.45], [0.28 + dy, 0.7 + dy], color=C["gray"], lw=0.7, zorder=2)

lab = dict(fontsize=8, color=C["ink"], arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.annotate("핵", xy=(-0.35, -0.25), xytext=(-0.55, -1.75), ha="center", **lab)
ax.annotate("인", xy=(-0.15, 0.12), xytext=(-0.05, 1.75), ha="center", **lab)
ax.annotate("거친면 소포체\n(니슬 소체)", xy=(-0.65, 0.85), xytext=(-1.9, 1.55), ha="center", **lab)
ax.annotate("골지체", xy=(0.75, -0.45), xytext=(1.35, -1.6), ha="center", **lab)
ax.annotate("미토콘드리아", xy=(0.95, 0.2), xytext=(1.25, 1.6), ha="center", **lab)
ax.annotate("미세소관", xy=(2.3, 0.03), xytext=(2.45, -0.75), ha="center", **lab)
ax.annotate("세포막", xy=(-1.0, -0.92), xytext=(-2.25, -1.6), ha="center", **lab)
ax.text(2.7, 0.3, "축삭 쪽", fontsize=7.5, color=C["gray"], ha="center")
ax.text(-2.7, 1.0, "수상돌기 쪽", fontsize=7.5, color=C["gray"], ha="center")
ax.plot([-1.88, -0.33], [-2.15, -2.15], color=C["ink"], lw=2)
ax.text(-1.1, -2.27, "약 10 μm", fontsize=7.5, ha="center", va="top")
ax.set_xlim(-3.1, 3.1)
ax.set_ylim(-2.6, 2.0)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("(가) 뉴런 세포체의 세포 소기관 (도식)", fontsize=9.5)

# ---- 오른쪽: 굵기 비교 (같은 축척, nm) ----
ax = a2
items = [(7, "액틴", C["red"]), (10, "신경미세섬유", C["green"]), (25, "미세소관", C["blue"])]
xs = [3, 25, 52]
for (d, name, col), xc in zip(items, xs):
    if d == 25:
        ax.add_patch(Circle((xc, 30), d / 2, fc="none", ec=col, lw=3.5))
        ax.add_patch(Circle((xc, 30), 7.5, fc="white", ec="none"))
    else:
        ax.add_patch(Circle((xc, 30), d / 2, fc=col, ec="none", alpha=0.75))
    ax.text(xc, 30 - 17, f"{name}\n약 {d} nm", ha="center", va="top", fontsize=7.8)
# 막 두께 막대
ax.add_patch(Rectangle((-2, 57), 66, 5, fc=C["green"], alpha=0.25, ec=C["green"], lw=0.8))
ax.text(31, 64, "지질 이중층 두께 약 5 nm (같은 축척)", ha="center", va="bottom", fontsize=7.8, color=C["green"])
ax.set_xlim(-4, 66)
ax.set_ylim(-12, 72)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("(나) 세포골격의 굵기 (단면, 같은 축척)", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
