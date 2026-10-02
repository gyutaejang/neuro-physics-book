from figstyle import plt, np, save, C
from matplotlib.patches import Polygon, Circle, FancyBboxPatch, Ellipse

fig, ax = plt.subplots(figsize=(7.3, 3.5))
G = C["green"]
rng = np.random.default_rng(3)


def branch(x, y, ang, length, depth, lw, spines=False):
    x2 = x + length * np.cos(ang)
    y2 = y + length * np.sin(ang)
    ax.plot([x, x2], [y, y2], color=G, lw=lw, solid_capstyle="round", zorder=2)
    if spines:
        for t in np.linspace(0.2, 0.9, 4):
            px, py = x + t * (x2 - x), y + t * (y2 - y)
            s = rng.choice([-1, 1])
            nx, ny = -np.sin(ang) * s, np.cos(ang) * s
            ax.plot([px, px + 0.07 * nx], [py, py + 0.07 * ny], color=G, lw=0.6, zorder=2)
            ax.add_patch(Circle((px + 0.09 * nx, py + 0.09 * ny), 0.025, fc=G, ec="none", zorder=2))
    if depth > 0:
        for d in (-0.45, 0.45):
            branch(x2, y2, ang + d + rng.normal(0, 0.1), length * 0.7, depth - 1, lw * 0.7, spines)


# 세포체 (삼각형에 가까운 피라미드 모양)
soma = Polygon([(2.0, 0.0), (2.75, 0.42), (2.75, -0.42)], closed=True, fc="#dcebd8", ec=G, lw=1.6, zorder=3)
ax.add_patch(soma)
ax.add_patch(Circle((2.5, 0.0), 0.13, fc="#b9d3b3", ec=G, lw=0.8, zorder=4))
# 꼭대기 수상돌기 (왼쪽으로 길게) + 끝 가지
ax.plot([0.25, 2.0], [0, 0], color=G, lw=2.6, zorder=2)
for a in (2.6, 3.3, 3.7):
    branch(0.25, 0.0, a, 0.45, 2, 1.4, spines=True)
for xb, a in [(1.1, 2.2), (1.4, -2.3)]:
    branch(xb, 0.0, a, 0.45, 1, 1.1, spines=True)
# 바닥 수상돌기
for a in (1.2, 1.9, -1.2, -1.9):
    branch(2.62, 0.3 * np.sign(a), a, 0.38, 1, 1.3, spines=True)

# 축삭 둔덕 + 초기분절
ax.add_patch(Polygon([(2.75, 0.14), (3.0, 0.05), (3.0, -0.05), (2.75, -0.14)], fc="#dcebd8", ec=G, lw=1.2, zorder=3))
ax.plot([3.0, 3.6], [0, 0], color=C["red"], lw=4, solid_capstyle="butt", zorder=3)
# 수초 마디와 결절
x0 = 3.65
for k in range(4):
    ax.add_patch(FancyBboxPatch((x0, -0.09), 0.62, 0.18, boxstyle="round,pad=0.01,rounding_size=0.08",
                                fc="#f2f2f2", ec=C["gray"], lw=1.0, zorder=3))
    x0 += 0.7
ax.plot([3.6, x0 + 0.1], [0, 0], color=G, lw=1.2, zorder=2)
# 곁가지와 종말
ax.plot([5.03, 5.4], [0.0, -0.55], color=G, lw=1.0, zorder=2)
ax.add_patch(Circle((5.42, -0.58), 0.05, fc=G, zorder=3))
xe = x0 + 0.1
for a in (0.6, 0.15, -0.3, -0.75):
    x2, y2 = xe + 0.55 * np.cos(a), 0.55 * np.sin(a)
    ax.plot([xe, x2], [0, y2], color=G, lw=1.0, zorder=2)
    ax.add_patch(Circle((x2, y2), 0.06, fc=G, ec="none", zorder=3))

# 확대 원: 가시 달린 수상돌기 (위쪽)
cx, cy, R = 1.0, 1.55, 0.42
ax.add_patch(Circle((cx, cy), R, fc="white", ec=C["gray"], lw=0.8, zorder=5))
ax.plot([cx - 0.35, cx + 0.35], [cy - 0.05, cy + 0.05], color=G, lw=4, zorder=6)
for t, s in [(-0.22, 1), (-0.05, -1), (0.12, 1), (0.27, -1)]:
    px, py = cx + t, cy + t / 7
    ax.plot([px, px], [py, py + s * 0.17], color=G, lw=1.0, zorder=6)
    ax.add_patch(Circle((px, py + s * 0.22), 0.055, fc=G, ec="none", zorder=6))
ax.plot([0.75, 0.6], [1.15, 0.45], color=C["gray"], lw=0.6, ls=":", zorder=1)
ax.text(cx + R + 0.06, cy + 0.2, "수상돌기 가시\n(흥분성 시냅스 대부분이\n여기에 맺힌다)", fontsize=7.6, va="center")

lab = dict(fontsize=8, ha="center", arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.annotate("꼭대기 수상돌기", xy=(1.5, 0.0), xytext=(1.55, -1.25), **lab)
ax.annotate("바닥 수상돌기", xy=(2.9, 0.62), xytext=(3.25, 1.2), **lab)
ax.annotate("세포체", xy=(2.45, -0.2), xytext=(2.5, -1.25), **lab)
ax.annotate("축삭 초기분절\n(활동전위 시작)", xy=(3.3, -0.03), xytext=(3.45, -1.25), **lab)
ax.annotate("수초", xy=(4.4, 0.09), xytext=(4.35, 0.95), **lab)
ax.annotate("랑비에 결절", xy=(4.98, 0.0), xytext=(5.3, 0.95), **lab)
ax.annotate("곁가지", xy=(5.25, -0.35), xytext=(4.75, -1.25), **lab)
ax.annotate("축삭 종말\n(시냅스 앞)", xy=(6.62, -0.4), xytext=(6.55, -1.25), **lab)

# 신호 방향
ax.annotate("", xy=(6.6, -1.85), xytext=(0.3, -1.85),
            arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.4, mutation_scale=12))
for xt, t in [(1.3, "입력 (시냅스 전위)"), (3.3, "통합 → 발화 결정"), (5.4, "출력 (활동전위 전도)")]:
    ax.text(xt, -1.75, t, ha="center", va="bottom", fontsize=8, color=C["blue"])
ax.set_xlim(-1.0, 7.25)
ax.set_ylim(-2.0, 2.05)
ax.set_aspect("equal")
ax.axis("off")
save(fig, __file__)
