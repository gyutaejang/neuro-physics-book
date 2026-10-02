from figstyle import plt, np, save, C
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Ellipse, Wedge

G, B, R, P, GR = C["green"], C["blue"], C["red"], C["purple"], C["gray"]
rng = np.random.default_rng(7)
fig, axes = plt.subplots(1, 4, figsize=(7.4, 3.3))


def twig(ax, x, y, ang, L, depth, lw, color, spread=0.5):
    x2, y2 = x + L * np.cos(ang), y + L * np.sin(ang)
    ax.plot([x, x2], [y, y2], color=color, lw=lw, solid_capstyle="round")
    if depth > 0:
        for d in (-spread, spread):
            twig(ax, x2, y2, ang + d + rng.normal(0, 0.2), L * 0.65, depth - 1, lw * 0.7, color, spread)


# (가) 성상세포: 혈관 종족 + 시냅스 감싸기
ax = axes[0]
ax.add_patch(Rectangle((-1.3, -1.55), 2.6, 0.55, fc="#f6dcc8", ec=R, lw=1.0))
ax.add_patch(Ellipse((-0.6, -1.27), 0.45, 0.28, fc=R, alpha=0.7, ec="none"))
ax.text(0.55, -1.27, "모세혈관", fontsize=7, ha="center", va="center", color=R)
ax.add_patch(Circle((0, 0.4), 0.17, fc="#cfe3cb", ec=G, lw=1.2, zorder=3))
for a in np.linspace(0, 2 * np.pi, 9, endpoint=False):
    if np.sin(a) < -0.6:
        continue
    twig(ax, 0.17 * np.cos(a), 0.4 + 0.17 * np.sin(a), a, 0.38, 2, 1.4, G, 0.55)
for xf in (-0.35, 0.35):
    ax.plot([0, xf], [0.25, -0.9], color=G, lw=2.0)
    ax.add_patch(FancyBboxPatch((xf - 0.22, -1.0), 0.44, 0.1, boxstyle="round,pad=0.01", fc=G, ec=G))
# 시냅스 (앞·뒤)와 감싸는 돌기
sx, sy = 0.75, 1.45
ax.add_patch(Circle((sx, sy + 0.12), 0.11, fc="white", ec=B, lw=1.0, zorder=4))
ax.add_patch(Circle((sx, sy - 0.12), 0.11, fc="white", ec=GR, lw=1.0, zorder=4))
ax.add_patch(Wedge((sx, sy), 0.24, 100, 260, width=0.06, fc=G, ec="none", zorder=4))
ax.plot([0.14, 0.53], [0.52, 1.4], color=G, lw=1.3)
ax.text(sx + 0.2, sy + 0.32, "시냅스", fontsize=6.8, ha="center", color=GR)
ax.text(0, 2.05, "K⁺ 완충 · 글루탐산 재흡수", ha="center", fontsize=7.2, color=G)
ax.set_title("(가) 성상세포", fontsize=9)
ax.text(0, -1.75, "돌기가 시냅스를 감싸고\n종족이 혈관을 덮는다", ha="center", va="top", fontsize=7.4)

# (나) 희소돌기아교세포: 여러 축삭에 수초
ax = axes[1]
ys = [1.35, 0.55, -0.25, -1.05]
for yy in ys:
    ax.plot([-1.3, 1.3], [yy, yy], color=G, lw=1.0)
for k, yy in enumerate(ys):
    xs = 0.15 if k % 2 else -0.35
    ax.add_patch(FancyBboxPatch((xs, yy - 0.09), 0.75, 0.18, boxstyle="round,pad=0.01,rounding_size=0.08",
                                fc="#f2f2f2", ec=GR, lw=0.9, zorder=3))
    ax.plot([-0.9, xs + 0.37], [0.15, yy], color=P, lw=0.9, zorder=2)
ax.add_patch(Circle((-0.9, 0.15), 0.16, fc="#e6def1", ec=P, lw=1.2, zorder=4))
ax.text(0, 1.75, "축삭", ha="center", fontsize=7.2, color=G)
ax.set_title("(나) 희소돌기아교세포", fontsize=9)
ax.text(0, -1.75, "세포 하나가 수십 개 축삭\n마디에 수초를 감는다", ha="center", va="top", fontsize=7.4)

# (다) 미세아교세포: 가늘게 갈라진 돌기
ax = axes[2]
ax.add_patch(Ellipse((0, 0.2), 0.32, 0.22, angle=20, fc="#dbe6f3", ec=B, lw=1.2, zorder=3))
for a in np.linspace(0, 2 * np.pi, 6, endpoint=False) + 0.3:
    twig(ax, 0.12 * np.cos(a), 0.2 + 0.1 * np.sin(a), a, 0.45, 3, 1.1, B, 0.55)
ax.add_patch(Circle((0.95, 1.25), 0.1, fc="white", ec=GR, lw=0.9))
ax.annotate("", xy=(0.85, 1.15), xytext=(0.55, 0.85),
            arrowprops=dict(arrowstyle="-|>", color=R, lw=1.0, mutation_scale=8))
ax.text(0, 2.05, "끊임없이 주변을 훑는다", ha="center", fontsize=7.2, color=B)
ax.set_title("(다) 미세아교세포", fontsize=9)
ax.text(0, -1.75, "면역 감시, 손상 반응,\n시냅스 가지치기", ha="center", va="top", fontsize=7.4)

# (라) NG2 세포 (희소돌기아교 전구세포)
ax = axes[3]
ax.add_patch(Circle((0, 0.2), 0.15, fc="#efe6d0", ec=GR, lw=1.2, zorder=3))
for a in np.linspace(0, 2 * np.pi, 5, endpoint=False) + 0.5:
    twig(ax, 0.15 * np.cos(a), 0.2 + 0.15 * np.sin(a), a, 0.5, 1, 1.2, GR, 0.4)
ax.annotate("", xy=(0.9, -1.0), xytext=(0.17, -0.07),
            arrowprops=dict(arrowstyle="-|>", color=P, lw=1.2, mutation_scale=9))
ax.add_patch(Circle((1.0, -1.1), 0.12, fc="#e6def1", ec=P, lw=1.0))
ax.text(0.62, -0.42, "분화", fontsize=7, color=P)
ax.plot([-1.3, -0.2], [1.3, 0.33], color=B, lw=1.0)
ax.add_patch(Circle((-0.19, 0.32), 0.06, fc=B, ec="none", zorder=4))
ax.text(-1.25, 1.45, "축삭 (시냅스 입력)", fontsize=6.8, color=B)
ax.text(0, 2.05, "평생 분열한다", ha="center", fontsize=7.2, color=GR)
ax.set_title("(라) NG2 세포", fontsize=9)
ax.text(0, -1.75, "새 희소돌기아교세포를 만들고\n뉴런에게서 시냅스를 받는다", ha="center", va="top", fontsize=7.4)

for ax in axes:
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-2.4, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout(w_pad=0.2)
save(fig, __file__)
