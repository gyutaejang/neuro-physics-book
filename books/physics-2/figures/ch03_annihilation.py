from matplotlib.patches import Circle, Rectangle, Ellipse
from figstyle import plt, np, save, C

# (가) 양전자 방출에서 소멸까지, (나) 링 검출기에서의 참·산란·우연 동시 계수
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.6), gridspec_kw=dict(width_ratios=[1, 1.08]))

# (가)
nuc = np.array([-1.35, -0.1])
pts = np.array([[0, 0], [0.18, 0.1], [0.3, -0.05], [0.45, 0.12], [0.55, 0.02], [0.7, 0.2],
                [0.82, 0.08], [0.95, 0.22], [1.08, 0.05], [1.2, 0.15], [1.3, 0.02]])
path = nuc + pts
a1.add_patch(Circle(nuc, 0.12, color=C["red"], zorder=3))
a1.text(nuc[0], nuc[1] - 0.3, "¹⁸F 원자핵", ha="center", va="top", fontsize=8.5)
a1.plot(path[:, 0], path[:, 1], color=C["blue"], lw=1.2)
a1.text(-0.8, 0.42, "양전자 e⁺", fontsize=8, color=C["blue"], ha="center")
end = path[-1]
a1.scatter([end[0]], [end[1]], marker="*", s=150, color=C["purple"], zorder=4)
yb = -0.85
a1.annotate("", xy=(end[0], yb), xytext=(nuc[0], yb),
            arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.8))
for xx in (nuc[0], end[0]):
    a1.plot([xx, xx], [yb - 0.06, yb + 0.06], color=C["gray"], lw=0.6)
a1.text(nuc[0] - 0.3, yb - 0.12, "양전자 비정\n(¹⁸F 평균 약 0.6 mm)", ha="left", va="top",
        fontsize=8, color=C["gray"])
ang = np.radians(78)
L = 1.45
for s in (1, -1):
    dx, dy = s * L * np.cos(ang), s * L * np.sin(ang)
    a1.annotate("", xy=(end[0] + dx, end[1] + dy), xytext=(end[0], end[1]),
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.6, mutation_scale=12))
    a1.text(end[0] + dx + 0.1, end[1] + dy - (0.05 if s > 0 else -0.1), "γ 511 keV",
            ha="left", va="center", fontsize=8.5, color=C["red"])
a1.text(end[0] + 0.28, end[1] - 0.05, "소멸 지점", fontsize=8.5, color=C["purple"], va="center")
a1.text(end[0] + 0.28, end[1] + 0.55, "거의 정반대로\n(180° ± 약 0.25°)", fontsize=8, va="center")
a1.text(-1.65, 1.35, "e⁺ + e⁻ → γ + γ", fontsize=9)
a1.set_xlim(-1.75, 1.75)
a1.set_ylim(-1.6, 1.6)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("(가) 양전자 방출과 소멸", fontsize=9.5)

# (나) 링
R = 1.0
nb = 36
for k in range(nb):
    th = 2 * np.pi * k / nb
    a2.add_patch(Rectangle((R * np.cos(th), R * np.sin(th)), 0.16, 0.14, angle=np.degrees(th) - 90 + 0,
                           rotation_point="xy", facecolor=C["light"], edgecolor=C["gray"], lw=0.5))
a2.add_patch(Ellipse((0, 0), 1.05, 1.25, facecolor="#f4efe6", edgecolor=C["gray"], lw=0.8))


def onring(th):
    return np.array([np.cos(th), np.sin(th)]) * (R + 0.07)


# 참 동시 계수
p = np.array([-0.15, 0.2])
d = np.array([np.cos(np.radians(20)), np.sin(np.radians(20))])
def hit(p, d):
    b = p @ d
    s = -b + np.sqrt(b * b - (p @ p - (R + 0.07) ** 2))
    return p + s * d
h1, h2 = hit(p, d), hit(p, -d)
a2.plot([h1[0], h2[0]], [h1[1], h2[1]], color=C["blue"], lw=1.6)
a2.scatter(*p, color=C["blue"], s=22, zorder=4)
# 산란
q = np.array([0.15, -0.25])
d1 = np.array([np.cos(np.radians(-75)), np.sin(np.radians(-75))])
e1 = hit(q, -d1)
k = q + 0.32 * d1
d2 = np.array([np.cos(np.radians(-35)), np.sin(np.radians(-35))])
e2 = hit(k, d2)
a2.plot([e1[0], q[0], k[0], e2[0]], [e1[1], q[1], k[1], e2[1]], color=C["red"], lw=1.3)
a2.plot([e1[0], e2[0]], [e1[1], e2[1]], color=C["red"], lw=0.9, ls="--")
a2.scatter(*q, color=C["red"], s=22, zorder=4)
a2.scatter(*k, color=C["red"], s=14, marker="x", zorder=4)
# 우연
for pp, ang_ in ((np.array([-0.3, -0.3]), 200), (np.array([0.3, 0.35]), 70)):
    dd = np.array([np.cos(np.radians(ang_)), np.sin(np.radians(ang_))])
    hh = hit(pp, dd)
    a2.plot([pp[0], hh[0]], [pp[1], hh[1]], color=C["gray"], lw=1.1)
    a2.scatter(*pp, color=C["gray"], s=18, zorder=4)
    a2.plot([pp[0], pp[0] - 0.12 * dd[0]], [pp[1], pp[1] - 0.12 * dd[1]], color=C["gray"], lw=0.6, ls=":")
hA = hit(np.array([-0.3, -0.3]), np.array([np.cos(np.radians(200)), np.sin(np.radians(200))]))
hB = hit(np.array([0.3, 0.35]), np.array([np.cos(np.radians(70)), np.sin(np.radians(70))]))
a2.plot([hA[0], hB[0]], [hA[1], hB[1]], color=C["gray"], lw=0.9, ls="--")
a2.set_xlim(-1.35, 2.25)
a2.set_ylim(-1.35, 1.35)
a2.set_aspect("equal")
a2.axis("off")
ty = 0.95
for col, ls, txt in ((C["blue"], "-", "참 동시 계수"), (C["red"], "--", "산란: 꺾인 경로,\n잘못된 응답선"),
                     (C["gray"], "--", "우연: 다른 두 소멸의\n광자가 우연히 짝지음")):
    a2.plot([1.32, 1.52], [ty, ty], color=col, ls=ls, lw=1.3)
    a2.text(1.58, ty, txt, fontsize=7.8, va="center" if "\n" not in txt else "top")
    ty -= 0.62
a2.set_title("(나) 링 검출기와 세 종류의 동시 계수", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
