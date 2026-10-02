from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle

# 반지름 a, 길이 L인 솔레노이드를 원형 고리 여러 개로 근사하고
# 비오-사바르 법칙으로 xz 평면(y = 0)의 자기장을 계산한다.
a, L, n_loops, n_seg = 0.35, 1.6, 24, 72
zs = np.linspace(-L / 2, L / 2, n_loops)
phi = np.linspace(0, 2 * np.pi, n_seg, endpoint=False)
dphi = 2 * np.pi / n_seg
SX, SY = a * np.cos(phi), a * np.sin(phi)
DLX, DLY = -a * np.sin(phi) * dphi, a * np.cos(phi) * dphi


def field(x, z):
    bx = bz = 0.0
    for z0 in zs:
        rx, ry, rz = x - SX, -SY, z - z0
        r3 = (rx**2 + ry**2 + rz**2) ** 1.5
        bx += np.sum(DLY * rz / r3)
        bz += np.sum((DLX * ry - DLY * rx) / r3)
    return bx, bz


def trace(x0, z0, step=0.02, nmax=1500, sgn=1):
    """자기력선 하나를 따라간다. z = 0을 다시 지나 출발점으로 돌아오거나 상자를 벗어나면 멈춘다."""
    pts = [(x0, z0)]
    x, z = x0, z0
    for i in range(nmax):
        bx, bz = field(x, z)
        n = sgn * np.hypot(bx, bz)
        xm, zm = x + 0.5 * step * bx / n, z + 0.5 * step * bz / n
        bx, bz = field(xm, zm)
        n = sgn * np.hypot(bx, bz)
        x, z = x + step * bx / n, z + step * bz / n
        pts.append((x, z))
        if abs(x) > 3.5 or abs(z) > 3.5:
            break
        if i > 20 and abs(x - x0) < 0.03 and abs(z - z0) < 0.03:
            break
    return np.array(pts)


lines = []
for s in (0.05, 0.13, 0.21, 0.28):
    for sgn in (1, -1):
        fwd = trace(sgn * s, 0.0)
        if np.hypot(*(fwd[-1] - fwd[0])) < 0.05:   # 닫힌 고리
            lines.append(fwd)
        else:                                       # 상자 밖으로 나가면 뒤쪽도 따라간다
            bwd = trace(sgn * s, 0.0, sgn=-1)
            lines.append(np.vstack([bwd[::-1], fwd[1:]]))

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
for ax in axes:
    for p in lines:
        ax.plot(p[:, 0], p[:, 1], color=C["purple"], lw=1.0)
        # 바깥쪽에서 z = 0을 지나는 곳에 아래 방향 화살표
        cross = (np.sign(p[:-1, 1]) != np.sign(p[1:, 1])) & (np.abs(p[:-1, 0]) > a + 0.05)
        idx = [j for j in np.where(cross)[0] if 0 < j < len(p) - 2]
        for j in idx[:1]:
            ax.annotate("", xy=p[j + 1], xytext=p[j - 1],
                        arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.0, mutation_scale=11))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axis("off")

# (가) 막대자석: 위가 N극
ax = axes[0]
ax.add_patch(Rectangle((-a, 0), 2 * a, L / 2, color=C["red"], zorder=3))
ax.add_patch(Rectangle((-a, -L / 2), 2 * a, L / 2, color=C["blue"], zorder=3))
ax.text(0, L / 4, "N", color="white", ha="center", va="center", fontsize=13, zorder=4)
ax.text(0, -L / 4, "S", color="white", ha="center", va="center", fontsize=13, zorder=4)
ax.text(0, -2.05, "바깥: N극에서 나와 S극으로", ha="center", va="top", fontsize=8.5, color=C["purple"])
ax.set_title("(가) 막대자석", fontsize=10.5)

# (나) 솔레노이드: 도선 단면 (왼쪽 ● 나옴, 오른쪽 × 들어감). 위에서 보아 시계 반대 방향 전류 → 안쪽 B는 위로
ax = axes[1]
for z0 in zs[::2]:
    ax.plot([-a], [z0], "o", ms=3.2, color=C["ink"], zorder=4)
    ax.plot([a], [z0], "x", ms=3.2, color=C["ink"], mew=1.0, zorder=4)
for s in (-0.19, 0.0, 0.19):
    ax.annotate("", xy=(s, 0.25), xytext=(s, -0.15),
                arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.2, mutation_scale=11))
ax.text(0, -2.05, "안쪽: 거의 균일하고 나란한 자기장", ha="center", va="top", fontsize=8.5, color=C["purple"])
ax.set_title("(나) 솔레노이드 (전류 고리를 쌓은 것)", fontsize=10.5)
save(fig, __file__)
