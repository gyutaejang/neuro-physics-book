from figstyle import plt, np, save, C


def charge(ax, x, y, sign):
    ax.add_patch(plt.Circle((x, y), 0.16, facecolor="white", edgecolor=C["ink"], lw=1.2, zorder=5))
    ax.text(x, y, "+" if sign > 0 else "−", ha="center", va="center", fontsize=12,
            weight="bold", color=C["ink"], zorder=6)


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.4))

# 왼쪽: 양전하 하나
for th in np.linspace(0, 2 * np.pi, 16, endpoint=False):
    x0, y0 = 0.2 * np.cos(th), 0.2 * np.sin(th)
    x1, y1 = 1.9 * np.cos(th), 1.9 * np.sin(th)
    a1.plot([x0, x1], [y0, y1], color=C["blue"], lw=1)
    a1.annotate("", xy=(1.25 * np.cos(th), 1.25 * np.sin(th)), xytext=(1.05 * np.cos(th), 1.05 * np.sin(th)),
                arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1, mutation_scale=9))
charge(a1, 0, 0, +1)
a1.set_title("양전하 하나: 바깥으로 퍼진다")
a1.text(0.5, -0.04, "선이 촘촘한 곳 = 전기장이 센 곳", ha="center", va="top", fontsize=8.5, color=C["gray"],
        transform=a1.transAxes)

# 오른쪽: 쌍극자
d = 0.6


def field(x, y):
    ex = ey = 0
    for q, cx in ((1, d), (-1, -d)):
        rx, ry = x - cx, y
        r3 = (rx ** 2 + ry ** 2) ** 1.5 + 1e-9
        ex = ex + q * rx / r3
        ey = ey + q * ry / r3
    return ex, ey




def trace(x, y, ds=0.01, nmax=4000):
    pts = [(x, y)]
    for _ in range(nmax):
        ex, ey = field(x, y)
        n = np.hypot(ex, ey)
        x, y = x + ds * ex / n, y + ds * ey / n
        pts.append((x, y))
        if np.hypot(x + d, y) < 0.16 or np.hypot(x, y) > 9:
            break
    return np.array(pts)


for th in np.linspace(0, 2 * np.pi, 18, endpoint=False):
    p = trace(d + 0.17 * np.cos(th), 0.17 * np.sin(th))
    a2.plot(p[:, 0], p[:, 1], color=C["blue"], lw=1)
    # 선 길이의 중간쯤(보이는 범위 안)에 화살촉
    inside = (abs(p[:, 0]) < 1.8) & (abs(p[:, 1]) < 1.8)
    out = np.where(~inside)[0]
    first = out[0] if len(out) else len(p)  # 처음 화면 밖으로 나가기 전까지
    i = int(first * 0.55) if first > 10 else None
    if i is not None and i + 1 < len(p):
        a2.annotate("", xy=p[i + 1], xytext=p[i - 5],
                    arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1, mutation_scale=9))
charge(a2, d, 0, +1)
charge(a2, -d, 0, -1)
a2.set_title("쌍극자: +에서 나와 −로 들어간다")
a2.text(0.5, -0.04, "멀어지면 두 전하의 효과가 서로 지운다", ha="center", va="top", fontsize=8.5, color=C["gray"],
        transform=a2.transAxes)

for a in (a1, a2):
    a.set_xlim(-2.2, 2.2)
    a.set_ylim(-2.2, 2.2)
    a.set_aspect("equal")
    a.axis("off")
fig.tight_layout()
save(fig, __file__)
