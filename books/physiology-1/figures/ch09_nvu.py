from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Rectangle

from figstyle import plt, np, save, C

# 신경혈관 단위 도식: 연질막 동맥 → 관통 세동맥(평활근) → 모세혈관(주피세포) → 세정맥.
fig, ax = plt.subplots(figsize=(7.2, 3.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.set_aspect("equal")
ax.axis("off")
art, ven = C["red"], C["purple"]

# 뇌 표면
ax.add_patch(Rectangle((0, 4.75), 10, 0.85, color="#f6f2ea", zorder=0))
ax.text(9.9, 5.45, "연질막(뇌 표면)", ha="right", va="center", fontsize=7.5, color=C["gray"])
# 연질막 동맥과 정맥
ax.add_patch(FancyBboxPatch((0.2, 4.9), 3.2, 0.35, boxstyle="round,pad=0,rounding_size=0.17",
                            fc="#f3d3c4", ec=art, lw=1.2))
ax.text(0.35, 5.07, "연질막 동맥", fontsize=7.5, va="center", color=art)
ax.add_patch(FancyBboxPatch((7.0, 4.9), 2.7, 0.35, boxstyle="round,pad=0,rounding_size=0.17",
                            fc="#ddd3ec", ec=ven, lw=1.2))
ax.text(7.15, 5.07, "피질 정맥", fontsize=7.5, va="center", color=ven)

# 관통 세동맥 (x = 2.3)
ax.add_patch(Rectangle((2.1, 1.9), 0.4, 3.05, fc="#f3d3c4", ec=art, lw=1.0))
for y in np.arange(2.15, 4.85, 0.22):  # 평활근 고리
    ax.add_patch(Rectangle((2.02, y), 0.56, 0.09, fc=C["gray"], ec="none", alpha=0.75))
# 모세혈관: 세동맥 아래에서 오른쪽으로 구불구불
xs = np.linspace(2.3, 8.9, 300)
ys = 1.55 + 0.25 * np.sin((xs - 2.3) * 1.25)
ax.plot(xs, ys, color="#c9a9b8", lw=6.5, solid_capstyle="round", zorder=1)
ax.plot(xs, ys, color=C["ink"], lw=0.5, zorder=2)
ax.plot([2.3, 2.3], [1.9, 1.6], color="#c9a9b8", lw=6.5, zorder=1)
# 주피세포 (모세혈관 위의 혹)
for xp in (3.6, 5.4, 6.9):
    yp = 1.55 + 0.25 * np.sin((xp - 2.3) * 1.25)
    ax.add_patch(Ellipse((xp, yp + 0.13), 0.42, 0.2, fc=C["green"], ec="none", alpha=0.85, zorder=3))
    ax.plot([xp - 0.35, xp + 0.35], [yp + 0.08, yp + 0.08], color=C["green"], lw=1.2, zorder=3)
# 세정맥 (x = 8.1)
ax.add_patch(Rectangle((8.9, 1.4), 0.45, 3.55, fc="#ddd3ec", ec=ven, lw=1.0))

# 성상세포
cx, cy = 4.4, 3.05
ax.add_patch(Ellipse((cx, cy), 0.55, 0.45, fc="#b9d6b2", ec=C["green"], lw=1, zorder=4))
for (x2, y2) in ((2.62, 3.4), (2.62, 2.6), (4.2, 1.85), (5.6, 3.7), (5.2, 2.4), (3.9, 4.1)):
    ax.plot([cx, x2], [cy, y2], color=C["green"], lw=1.6, zorder=3)
for (x2, y2) in ((2.62, 3.4), (2.62, 2.6)):  # 종족
    ax.add_patch(Ellipse((x2, y2), 0.16, 0.42, fc="#b9d6b2", ec=C["green"], lw=0.8, zorder=4))
ax.add_patch(Ellipse((4.2, 1.83), 0.42, 0.14, fc="#b9d6b2", ec=C["green"], lw=0.8, zorder=4))

# 뉴런 (피라미드) 과 시냅스
ax.add_patch(Polygon([[6.3, 2.75], [6.9, 2.75], [6.6, 3.45]], fc="#cfe3c9", ec=C["green"], lw=1.2, zorder=4))
ax.plot([6.6, 6.6], [3.45, 4.6], color=C["green"], lw=1.4)  # 첨단 수상돌기
ax.plot([6.6, 6.2], [4.1, 4.45], color=C["green"], lw=1.0)
ax.plot([6.6, 6.6], [2.75, 2.15], color=C["green"], lw=1.0)  # 축삭
ax.plot([6.35, 5.9], [2.8, 2.45], color=C["green"], lw=1.0)
ax.add_patch(plt.Circle((5.75, 3.78), 0.09, color=C["ink"], zorder=5))  # 시냅스
ax.plot([5.75, 6.6], [3.78, 3.95], color=C["ink"], lw=0.8)

# 이름표
def lab(xy, txt, xt, col=C["ink"], ha="left"):
    ax.annotate(txt, xy=xy, xytext=xt, fontsize=8, color=col, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))

lab((2.0, 4.3), "관통 세동맥\n(평활근 고리)", (0.15, 4.1), art)
lab((2.1, 2.2), "내피세포\n(혈관 안쪽 벽)", (0.15, 2.5))
lab((2.6, 3.4), "성상세포 종족", (3.0, 4.45), C["green"])
lab((cx - 0.15, cy - 0.1), "성상세포", (3.15, 2.45), C["green"])
lab((5.4, 1.77), "주피세포", (5.05, 0.6), C["green"])
lab((3.1, 1.5), "모세혈관", (2.5, 0.6), C["ink"])
lab((6.75, 3.1), "뉴런", (7.2, 3.3), C["green"])
lab((5.75, 3.78), "시냅스", (5.0, 4.45))
lab((8.9, 2.4), "세정맥\n(탈산소Hb↑)", (7.45, 2.1), ven)
ax.annotate("", xy=(9.12, 4.6), xytext=(9.12, 2.0),
            arrowprops=dict(arrowstyle="-|>", color=ven, lw=1.0, mutation_scale=9))
ax.annotate("", xy=(2.3, 2.2), xytext=(2.3, 4.6),
            arrowprops=dict(arrowstyle="-|>", color=art, lw=1.0, mutation_scale=9))
ax.text(9.9, 0.3, "도식(크기 비율은 실제와 다름). 모세혈관 사이 간격 약 40–60 μm", ha="right", fontsize=7.5, color=C["gray"])
save(fig, __file__)
