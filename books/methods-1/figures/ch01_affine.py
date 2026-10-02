from figstyle import plt, np, save, C

# 2차원으로 줄여 그린 아핀 변환: 복셀 번호 (i, j) → 세계 좌표 (x, y) mm.
# 3 mm 복셀, 15° 기울임, x축 뒤집힘(번호가 커질수록 왼쪽), 평행이동.
vox = 3.0
ang = np.deg2rad(15)
R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
M = R @ np.diag([-vox, vox])
t = np.array([12.0, -9.0])
ni, nj = 8, 6
pick = (5, 2)


def to_world(i, j):
    return M @ np.array([i, j]) + t


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.62))

# (가) 복셀 공간
for i in range(ni):
    for j in range(nj):
        hl = (i, j) == pick
        a1.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, fc=C["red"] if hl else C["light"],
                                   ec=C["gray"], lw=0.6, alpha=0.9 if hl else 1))
a1.plot(0, 0, "o", color=C["blue"], ms=5)
a1.annotate("", xy=(2.2, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=C["blue"], lw=1.6))
a1.annotate("", xy=(0, 2.2), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=C["blue"], lw=1.6))
a1.text(2.3, -0.15, "i", color=C["blue"], fontsize=11, va="top")
a1.text(-0.15, 2.3, "j", color=C["blue"], fontsize=11, ha="right")
a1.text(pick[0], pick[1] + 0.95, "(5, 2)", ha="center", fontsize=9, color=C["red"])
a1.set_xlim(-1, ni); a1.set_ylim(-1, nj)
a1.set_aspect("equal")
a1.set_xticks(range(ni)); a1.set_yticks(range(nj))
a1.set_xlabel("복셀 번호 i")
a1.set_ylabel("복셀 번호 j")
a1.set_title("(가) 배열 속 자리: 번호만 있다", fontsize=10)

# (나) 세계 공간
for i in range(ni):
    for j in range(nj):
        corners = np.array([to_world(i + di, j + dj) for di, dj in [(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5)]])
        hl = (i, j) == pick
        a2.add_patch(plt.Polygon(corners, fc=C["red"] if hl else C["light"], ec=C["gray"], lw=0.6))
o = to_world(0, 0)
ei, ej = to_world(2.2, 0) - o, to_world(0, 2.2) - o
a2.annotate("", xy=o + ei, xytext=o, arrowprops=dict(arrowstyle="->", color=C["blue"], lw=1.6))
a2.annotate("", xy=o + ej, xytext=o, arrowprops=dict(arrowstyle="->", color=C["blue"], lw=1.6))
a2.text(*(o + ei * 1.12), "i", color=C["blue"], fontsize=11, ha="right", va="top")
a2.text(*(o + ej * 1.1), "j", color=C["blue"], fontsize=11, ha="left")
p = to_world(*pick)
a2.annotate(f"({p[0]:.1f}, {p[1]:.1f}) mm", xy=p, xytext=(-18, -20), fontsize=9,
            color=C["red"], ha="center", arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.8))
a2.axhline(0, color=C["gray"], lw=0.8, ls=":")
a2.axvline(0, color=C["gray"], lw=0.8, ls=":")
a2.plot(0, 0, "+", color=C["ink"], ms=9)
a2.text(1.2, 1.2, "원점", fontsize=8.5, bbox=dict(fc="white", ec="none", pad=0.5))
a2.set_aspect("equal")
a2.set_xlim(-30, 18); a2.set_ylim(-24, 14)
a2.set_xlabel("x (mm, 오른쪽 +)")
a2.set_ylabel("y (mm, 앞쪽 +)")
a2.set_title("(나) 머리 속 자리: mm 좌표", fontsize=10)
b1, b2 = a1.get_position(), a2.get_position()
xm0, xm1 = b1.x1 + 0.015, b2.x0 - 0.075
ym = (b1.y0 + b1.y1) / 2
fig.text((xm0 + xm1) / 2, ym + 0.06, "아핀 행렬 A", ha="center", va="bottom", fontsize=9.5, color=C["ink"])
fig.patches.append(plt.matplotlib.patches.FancyArrowPatch((xm0, ym), (xm1, ym), transform=fig.transFigure,
                   arrowstyle="-|>", mutation_scale=14, color=C["ink"]))
save(fig, __file__)
