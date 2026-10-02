from figstyle import plt, np, save, C


def wire(ax, *pts, **kw):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=kw.get("color", C["ink"]), lw=1.4, solid_capstyle="round")


def resistor(ax, p0, p1, n=6, w=0.13, color=None):
    """p0에서 p1까지 지그재그 저항. 양 끝 20%는 도선."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    nrm = np.array([-u[1], u[0]])
    a, b = p0 + 0.2 * d, p0 + 0.8 * d
    pts = [p0, a]
    for k in range(1, 2 * n):
        t = k / (2 * n)
        pts.append(a + t * (b - a) + nrm * w * (1 if k % 2 else -1))
    pts += [b, p1]
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color or C["ink"], lw=1.4)


def battery(ax, x, y0, y1, label):
    """세로 방향 전지. 위가 +극(긴 선)."""
    ym = (y0 + y1) / 2
    wire(ax, (x, y0), (x, ym - 0.08))
    wire(ax, (x, ym + 0.08), (x, y1))
    ax.plot([x - 0.22, x + 0.22], [ym + 0.08, ym + 0.08], color=C["ink"], lw=1.4)
    ax.plot([x - 0.12, x + 0.12], [ym - 0.08, ym - 0.08], color=C["ink"], lw=3)
    ax.text(x - 0.32, ym + 0.12, "+", fontsize=9, ha="center")
    ax.text(x - 0.45, ym - 0.05, label, fontsize=9, ha="right", va="center")


def arrow(ax, p0, p1, text, offset=(0, 0.15), color=None):
    color = color or C["red"]
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3))
    mx, my = (p0[0] + p1[0]) / 2 + offset[0], (p0[1] + p1[1]) / 2 + offset[1]
    ax.text(mx, my, text, color=color, fontsize=9, ha="center", va="center")


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))

# (가) 직렬
battery(a1, 0, 0, 2, "V")
wire(a1, (0, 2), (0.6, 2))
resistor(a1, (0.6, 2), (2.2, 2))
wire(a1, (2.2, 2), (2.6, 2))
resistor(a1, (2.6, 2), (2.6, 0.4))
wire(a1, (2.6, 0.4), (2.6, 0), (0, 0))
a1.text(1.4, 2.32, "$R_1$", ha="center", fontsize=10)
a1.text(1.4, 1.62, "$V_1 = IR_1$", ha="center", fontsize=8.5, color=C["blue"])
a1.text(2.85, 1.2, "$R_2$", va="center", fontsize=10)
a1.text(2.85, 0.85, "$V_2 = IR_2$", va="center", fontsize=8.5, color=C["blue"])
arrow(a1, (0.1, 2.0 + 0.0), (0.55, 2.0), "", color=C["red"])
a1.text(0.3, 2.25, "I", color=C["red"], fontsize=10, ha="center")
arrow(a1, (1.9, 0), (0.9, 0), "")
a1.text(1.4, -0.25, "모든 곳에서 같은 전류 I", color=C["red"], fontsize=8.5, ha="center", va="top")
a1.text(1.6, -0.75, "$R = R_1 + R_2$,   $V = V_1 + V_2$", fontsize=9.5, ha="center", va="top")
a1.set_title("(가) 직렬: 전류는 같고 전압이 나뉜다", fontsize=10)

# (나) 병렬
battery(a2, 0, 0, 2, "V")
wire(a2, (0, 2), (2.8, 2))
wire(a2, (0, 0), (2.8, 0))
resistor(a2, (1.5, 2), (1.5, 0))
resistor(a2, (2.8, 2), (2.8, 0))
a2.plot([1.5], [2], "o", color=C["ink"], ms=3.5)
a2.plot([1.5], [0], "o", color=C["ink"], ms=3.5)
a2.text(1.72, 1.0, "$R_1$", fontsize=10, va="center")
a2.text(3.02, 1.0, "$R_2$", fontsize=10, va="center")
arrow(a2, (0.25, 2), (0.85, 2), "")
a2.text(0.55, 2.25, "I", color=C["red"], fontsize=10, ha="center")
arrow(a2, (1.5 - 0.22, 1.75), (1.5 - 0.22, 1.25), "")
a2.text(1.12, 1.5, "$I_1$", color=C["red"], fontsize=9.5, ha="right", va="center")
arrow(a2, (2.8 - 0.22, 1.75), (2.8 - 0.22, 1.25), "")
a2.text(2.42, 1.5, "$I_2$", color=C["red"], fontsize=9.5, ha="right", va="center")
a2.text(1.6, -0.25, "모든 가지에 같은 전압 V", color=C["blue"], fontsize=8.5, ha="center", va="top")
a2.text(1.6, -0.75, "$g = g_1 + g_2$,   $I = I_1 + I_2$", fontsize=9.5, ha="center", va="top")
a2.set_title("(나) 병렬: 전압은 같고 전류가 나뉜다", fontsize=10)

for ax in (a1, a2):
    ax.set_xlim(-1.0, 3.8)
    ax.set_ylim(-1.2, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout()
save(fig, __file__)
