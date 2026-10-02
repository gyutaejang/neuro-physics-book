from figstyle import plt, np, save, C
from matplotlib.patches import Circle

fig, ax = plt.subplots(figsize=(7.0, 4.0))
red = C["red"]


def vessel(pts, lw, color=red, ls="-"):
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, solid_capstyle="round", ls=ls)


for s in (-1, 1):
    vessel([(0.75 * s, -4.3), (0.12 * s, -3.0)], 3.2)            # 척추동맥
    vessel([(0.15 * s, -0.9), (0.95 * s, -1.0), (2.4 * s, -1.9), (3.0 * s, -2.6)], 2.8)  # 후대뇌동맥
    vessel([(0.95 * s, -1.0), (1.05 * s, 0.55)], 1.6)              # 후교통동맥
    vessel([(1.05 * s, 0.55), (2.2 * s, 0.75), (3.4 * s, 1.15)], 3.6)  # 중대뇌동맥
    vessel([(1.05 * s, 0.55), (0.3 * s, 1.6), (0.3 * s, 3.1)], 2.6)  # 전대뇌동맥
    ax.add_patch(Circle((1.05 * s, 0.55), 0.24, fc="white", ec=red, lw=2.4, zorder=4))
vessel([(0, -3.0), (0, -0.9)], 4.0)                              # 기저동맥
vessel([(-0.3, 1.6), (0.3, 1.6)], 1.6)                            # 전교통동맥
vessel([(-0.15, -0.9), (0.15, -0.9)], 4.0)

# 고리 강조
ring = np.array([(-0.3, 1.6), (0.3, 1.6), (1.05, 0.55), (0.95, -1.0), (0.15, -0.9),
                 (-0.15, -0.9), (-0.95, -1.0), (-1.05, 0.55), (-0.3, 1.6)])
ax.fill(ring[:, 0], ring[:, 1], color=C["light"], zorder=0)

kw = dict(fontsize=8.5, color=C["ink"])
ax.text(0, 0.0, "윌리스 고리", ha="center", fontsize=9.5, color=C["blue"], weight="bold")
ax.text(0.45, 1.72, "전교통동맥", ha="left", va="bottom", **kw)
ax.text(0.42, 2.85, "전대뇌동맥", ha="left", **kw)
ax.text(3.45, 1.3, "중대뇌동맥", ha="center", va="bottom", **kw)
ax.text(1.38, 0.28, "내경동맥 (단면)", ha="left", va="top", **kw)
ax.text(1.18, -0.45, "후교통동맥", ha="left", va="center", **kw)
ax.text(2.95, -2.75, "후대뇌동맥", ha="center", va="top", **kw)
ax.text(0.15, -2.0, "기저동맥", ha="left", **kw)
ax.text(0.8, -4.25, "척추동맥", ha="left", **kw)

# 유입량 설명 (왼쪽)
ax.text(-7.6, 2.9, "앞쪽 순환: 내경동맥 2개\n뇌혈류의 약 70–80 %", fontsize=8.3, color=red, va="top")
ax.text(-7.6, -3.1, "뒤쪽 순환: 척추동맥 2개 → 기저동맥\n뇌혈류의 약 20–30 %", fontsize=8.3, color=red, va="top")
ax.text(-7.6, 1.2, "고리의 교통동맥이\n좌우·앞뒤를 잇는 곁길이다.\n교과서 모양 그대로 완전한\n고리는 절반이 안 된다.",
        fontsize=7.8, color=C["gray"], va="top")
ax.text(0, 3.45, "앞", ha="center", fontsize=8, color=C["gray"])
ax.text(0, -4.75, "뒤", ha="center", fontsize=8, color=C["gray"])
ax.set_xlim(-7.7, 4.3)
ax.set_ylim(-4.9, 3.7)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
save(fig, __file__)
