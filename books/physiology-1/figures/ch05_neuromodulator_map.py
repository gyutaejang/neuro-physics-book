from figstyle import plt, np, save, C
from matplotlib.patches import Ellipse, Polygon, FancyArrowPatch

# 정중 시상 단면을 단순화한 도식. 왼쪽이 앞(이마), 오른쪽이 뒤(뒤통수)다.
th = np.linspace(0, 2 * np.pi, 300)
cx = 5.0 * np.cos(th)
cy = np.where(np.sin(th) > 0, 3.3 * np.sin(th), 1.6 * np.sin(th))
cy = cy - 0.35 * np.exp(-((cx - 0.8) / 1.6) ** 2) * (np.sin(th) < 0)  # 아랫면의 오목한 곳
CEREBRUM = np.c_[cx, cy]
STEM = np.array([[0.2, -1.2], [1.6, -1.15], [2.0, -2.4], [2.15, -3.4], [2.25, -4.6],
                 [1.55, -4.6], [1.35, -3.4], [0.9, -2.4]])


def brain(ax):
    ax.add_patch(Polygon(CEREBRUM, closed=True, facecolor="#f4f4f4", edgecolor=C["gray"], lw=1))
    ax.add_patch(Polygon(STEM, closed=True, facecolor="#ececec", edgecolor=C["gray"], lw=1))
    ax.add_patch(Ellipse((3.75, -2.35), 3.0, 1.9, angle=-12, facecolor="#ececec",
                         edgecolor=C["gray"], lw=1))
    ax.add_patch(Ellipse((-0.9, 0.35), 1.9, 1.0, facecolor="white", edgecolor=C["gray"],
                         lw=0.6, ls=":"))
    ax.add_patch(Ellipse((0.6, -0.15), 1.3, 0.8, facecolor="white", edgecolor=C["gray"],
                         lw=0.6, ls=":"))
    ax.text(-0.9, 0.35, "선조체", ha="center", va="center", fontsize=8.8, color=C["gray"])
    ax.text(0.6, -0.15, "시상", ha="center", va="center", fontsize=8.8, color=C["gray"])
    ax.text(3.75, -2.45, "소뇌", ha="center", va="center", fontsize=8.8, color=C["gray"])
    ax.text(-4.6, 2.9, "앞", fontsize=8.5, color=C["gray"])
    ax.text(4.3, 2.9, "뒤", fontsize=8.5, color=C["gray"])
    ax.set_xlim(-5.3, 5.6)
    ax.set_ylim(-4.8, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")


def cortex_point(angle_deg, r=0.86):
    a = np.deg2rad(angle_deg)
    return (r * 5.0 * np.cos(a), r * 3.3 * np.sin(a))


def arrow(ax, p, q, col, rad=-0.25, lw=1.1):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=7, color=col, lw=lw, alpha=0.9))


def nucleus(ax, xy, col, label, dx=0.0, dy=-0.45, ha="center"):
    ax.scatter([xy[0]], [xy[1]], s=46, color=col, zorder=5, edgecolor="white", lw=0.6)
    if label:
        ax.text(xy[0] + dx, xy[1] + dy, label, ha=ha, va="top", fontsize=9.6, color=col, zorder=6,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.95, pad=0.6))


fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.4))
(a_da, a_ne), (a_5ht, a_ach) = axes
for a in axes.flat:
    brain(a)

# 도파민: 흑질 치밀부 → 등쪽 선조체, VTA → 배쪽 선조체·전전두 피질
col = C["blue"]
snc, vta = (1.15, -1.55), (0.55, -1.55)
arrow(a_da, snc, (-0.5, 0.4), col, rad=0.35, lw=1.6)
arrow(a_da, vta, (-1.3, 0.05), col, rad=0.2)
arrow(a_da, vta, cortex_point(160), col, rad=-0.15)
arrow(a_da, vta, cortex_point(135), col, rad=-0.2)
nucleus(a_da, snc, col, "흑질 치밀부", dx=0.25, dy=-0.25, ha="left")
nucleus(a_da, vta, col, "VTA", dx=-0.2, dy=-0.25, ha="right")
a_da.text(-4.35, 0.15, "전전두\n피질", fontsize=9.4, color=col, va="top",
          bbox=dict(facecolor="white", edgecolor="none", alpha=0.95, pad=0.6))
a_da.set_title("도파민: 흑질·배쪽 피개 영역(VTA)", fontsize=11.5, color=col)

# 노르에피네프린: 청반 → 피질 전체, 시상, 소뇌, 척수
col = C["red"]
lc = (2.0, -2.35)
for ang in (150, 115, 80, 45, 15):
    arrow(a_ne, lc, cortex_point(ang), col, rad=-0.25, lw=0.9)
arrow(a_ne, lc, (0.7, -0.2), col, rad=-0.2, lw=0.9)
arrow(a_ne, lc, (3.6, -2.0), col, rad=0.3, lw=0.9)
arrow(a_ne, lc, (1.95, -4.5), col, rad=0.1, lw=0.9)
nucleus(a_ne, lc, col, "청반", dx=0.2, dy=-0.3, ha="left")
a_ne.set_title("노르에피네프린: 청반", fontsize=11.5, color=col)

# 세로토닌: 등쪽·정중 봉선핵 → 앞뇌 전체, 꼬리 쪽 봉선핵 → 척수
col = C["green"]
dr, cr = (1.25, -1.95), (1.85, -3.6)
for ang in (155, 120, 85, 50, 20):
    arrow(a_5ht, dr, cortex_point(ang), col, rad=-0.2, lw=0.9)
arrow(a_5ht, dr, (-0.8, 0.1), col, rad=0.25, lw=0.9)
arrow(a_5ht, cr, (1.95, -4.55), col, rad=0.0, lw=0.9)
arrow(a_5ht, cr, (3.2, -2.9), col, rad=0.2, lw=0.9)
nucleus(a_5ht, dr, col, "등쪽·정중\n봉선핵", dx=-0.3, dy=-0.45, ha="right")
nucleus(a_5ht, cr, col, "꼬리 쪽\n봉선핵", dx=-0.3, dy=0.05, ha="right")
a_5ht.set_title("세로토닌: 봉선핵", fontsize=11.5, color=col)

# 아세틸콜린: 기저 전뇌(마이네르트 기저핵) → 피질, 중격 → 해마, 뇌줄기(PPT/LDT) → 시상
col = C["purple"]
nbm, sep, ppt = (-2.0, -1.0), (-2.35, -0.3), (1.55, -2.05)
for ang in (165, 130, 95, 60, 30):
    arrow(a_ach, nbm, cortex_point(ang), col, rad=-0.3, lw=0.9)
arrow(a_ach, sep, (2.2, -0.95), col, rad=-0.12, lw=0.9)
arrow(a_ach, ppt, (0.75, -0.3), col, rad=-0.3, lw=1.3)
nucleus(a_ach, nbm, col, "기저 전뇌\n(마이네르트 기저핵)", dy=-0.4)
nucleus(a_ach, sep, col, "", dy=0)
nucleus(a_ach, ppt, col, "PPT/LDT", dx=0.05, dy=-0.4)
a_ach.text(2.35, -0.85, "해마로", fontsize=9.4, color=col, va="center")
a_ach.text(-2.65, -0.3, "중격", fontsize=9.4, color=col, ha="right", va="center")
a_ach.set_title("아세틸콜린: 기저 전뇌·뇌줄기", fontsize=11.5, color=col)

fig.tight_layout(h_pad=0.4, w_pad=0.6)
save(fig, __file__)
