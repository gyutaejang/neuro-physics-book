from figstyle import plt, np, save, C
from matplotlib.patches import Polygon, Circle

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.6), gridspec_kw=dict(width_ratios=[1.35, 1]))

# 왼쪽: 피라미드 뉴런 하나와 세 종류의 인터뉴런
ax = a1
ax.set_xlim(-3.2, 3.6)
ax.set_ylim(-3.3, 4.3)
ax.axis("off")
ax.set_aspect("equal")
# 피질 층 표시
for y, lab in ((3.4, "1층"), (0.0, "2/3층")):
    ax.text(-3.1, y, lab, fontsize=9.0, color=C["gray"], va="center")
ax.axhline(2.9, xmin=0.02, xmax=0.98, color=C["gray"], lw=0.5, ls=":")

g = C["ink"]
ax.add_patch(Polygon([[-0.45, -0.35], [0.45, -0.35], [0, 0.45]], closed=True, facecolor="#dfe7f1",
                     edgecolor=g, lw=1.0, zorder=3))
ax.plot([0, 0], [0.45, 3.6], color=g, lw=1.6, zorder=2)              # 꼭대기 수상돌기
for sx in (-1, 1):
    ax.plot([0, sx * 0.9], [3.2, 3.95], color=g, lw=1.0)             # 1층 술 모양 가지
    ax.plot([sx * 0.35, sx * 1.1], [-0.3, -0.9], color=g, lw=1.0)    # 바닥 수상돌기
ax.plot([0, 0], [-0.35, -3.0], color=g, lw=0.9, ls="--")             # 축삭
ax.text(0.1, -3.05, "축삭 → 출력", fontsize=9.0, va="top")
ax.text(0.15, 1.6, "피라미드\n뉴런", fontsize=9.0, color=C["blue"])


def cell(x, y, col, name):
    ax.add_patch(Circle((x, y), 0.28, facecolor=col, edgecolor="white", lw=0.8, zorder=4))
    ax.text(x, y, name, ha="center", va="center", fontsize=7.8, color="white", zorder=5)


def inhib(p, q, col, lw=1.3, rad=0.0):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-[, widthB=0.35, lengthB=0.12",
                color=col, lw=lw, connectionstyle=f"arc3,rad={rad}"), zorder=3)


cell(-1.9, 0.0, C["red"], "PV")
inhib((-1.62, 0.0), (-0.42, 0.02), C["red"], lw=1.6)
inhib((-1.75, -0.24), (-0.1, -0.75), C["red"], rad=0.2)
ax.text(-1.9, 0.4, "세포체·축삭\n초기분절에", ha="center", va="bottom", fontsize=8.2, color=C["red"])

cell(1.8, 0.9, C["green"], "SST")
ax.plot([1.8, 1.8], [1.18, 3.55], color=C["green"], lw=0.9)
inhib((1.8, 3.55), (0.12, 3.5), C["green"], lw=1.4)
ax.text(1.95, 2.3, "축삭이 1층으로\n올라가 먼 수상돌기에", fontsize=8.2, color=C["green"])

cell(2.9, -1.1, C["purple"], "VIP")
inhib((2.75, -0.85), (1.95, 0.65), C["purple"], lw=1.4)
ax.text(2.9, -1.5, "SST를 억제\n(탈억제)", ha="center", va="top", fontsize=8.2, color=C["purple"])


# 오른쪽: 피질 GABA 인터뉴런의 대략적 구성
ax = a2
groups = [("PV", 40, C["red"], "빠른 발화\n(바구니·샹들리에 세포)"),
          ("SST", 30, C["green"], "마르티노티 세포 등"),
          ("5HT3aR\n(VIP 포함)", 30, C["purple"], "VIP, 신경교 형태 세포 등")]
bottom = 0
for name, frac, col, note in groups:
    ax.bar(0, frac, bottom=bottom, width=0.45, color=col, alpha=0.85)
    ax.text(0, bottom + frac / 2, f"{name}\n약 {frac} %", ha="center", va="center", fontsize=9.0,
            color="white")
    ax.text(0.36, bottom + frac / 2, note, va="center", fontsize=8.6, color=col)
    bottom += frac
ax.set_xlim(-0.4, 1.35)
ax.set_ylim(0, 100)
ax.set_xticks([])
ax.set_ylabel("인터뉴런 중 비율 (%)")
ax.set_title("피질 뉴런의 약 20 %가 억제성", fontsize=11.4)
fig.tight_layout()
save(fig, __file__)
