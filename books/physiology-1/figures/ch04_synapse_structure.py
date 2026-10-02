from figstyle import plt, np, save, C
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Ellipse

fig, ax = plt.subplots(figsize=(6.8, 3.9))

# 시냅스 앞 종말 (위)
pre = FancyBboxPatch((1.0, 2.35), 5.0, 2.2, boxstyle="round,pad=0,rounding_size=0.9",
                     facecolor=C["light"], edgecolor=C["blue"], lw=1.3)
ax.add_patch(pre)
# 축삭 줄기
ax.add_patch(Rectangle((3.15, 4.4), 0.7, 0.6, facecolor=C["light"], edgecolor="none"))
ax.plot([3.15, 3.15], [4.45, 5.0], color=C["blue"], lw=1.3)
ax.plot([3.85, 3.85], [4.45, 5.0], color=C["blue"], lw=1.3)
ax.text(4.0, 4.85, "축삭", fontsize=8.5, va="center")

# 소포
rng = np.random.default_rng(3)
pts = []
while len(pts) < 22:
    x, y = rng.uniform(1.6, 5.4), rng.uniform(3.0, 3.85)
    if all(np.hypot(x - a, y - b) > 0.34 for a, b in pts):
        pts.append((x, y))
for x, y in pts:
    ax.add_patch(Circle((x, y), 0.14, facecolor="white", edgecolor=C["green"], lw=1.0))
# 결합된(도킹) 소포
for x in (2.75, 3.25, 3.75, 4.25):
    ax.add_patch(Circle((x, 2.53), 0.14, facecolor=C["green"], edgecolor=C["green"], alpha=0.75))
# 활성대 (치밀한 막)
ax.plot([2.5, 4.5], [2.36, 2.36], color=C["ink"], lw=3.2, solid_capstyle="butt")
# Ca 통로
for x in (2.5, 3.0, 3.5, 4.0, 4.5):
    ax.add_patch(Rectangle((x - 0.06, 2.24), 0.12, 0.24, facecolor=C["red"], edgecolor="none"))
ax.annotate("", xy=(4.5, 2.62), xytext=(4.5, 2.05),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.0, mutation_scale=9))

# 시냅스 뒤 (아래)
post = FancyBboxPatch((1.0, -0.4), 5.0, 2.25, boxstyle="round,pad=0,rounding_size=0.6",
                      facecolor="#eef5ec", edgecolor=C["green"], lw=1.3)
ax.add_patch(post)
ax.add_patch(Rectangle((2.45, 1.47), 2.1, 0.36, facecolor=C["gray"], alpha=0.45, edgecolor="none"))
for x in np.linspace(2.6, 4.4, 6):
    ax.add_patch(Rectangle((x - 0.07, 1.72), 0.14, 0.26, facecolor=C["purple"], edgecolor="none"))

# 틈 표시
ax.annotate("", xy=(5.55, 2.35), xytext=(5.55, 1.85),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.9, mutation_scale=8))

# 성상세포 돌기 (오른쪽)
ax.add_patch(Ellipse((7.05, 2.1), 1.0, 2.3, facecolor="#f3ece2", edgecolor=C["gray"], lw=1.0))
for y in (1.45, 2.1, 2.75):
    ax.add_patch(Rectangle((6.5, y - 0.07), 0.2, 0.14, facecolor=C["green"], edgecolor="none"))

# 글자 (왼쪽 설명)
def lab(x, y, s, xt, yt, col=C["ink"]):
    ax.annotate(s, xy=(x, y), xytext=(xt, yt), fontsize=8.5, va="center", ha="right", color=col,
                arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))

lab(1.75, 3.7, "시냅스 소포\n(지름 약 40 nm)", 0.7, 3.95)
lab(2.75, 2.53, "막에 결합한 소포\n(즉시 방출 가능)", 0.7, 2.85, C["green"])
lab(2.5, 2.30, "활성대와 Ca²⁺ 통로", 0.7, 2.05, C["red"])
lab(2.6, 1.78, "수용체", 0.7, 1.55, C["purple"])
lab(2.45, 1.55, "시냅스 뒤 밀도 (PSD)", 0.7, 1.05)
ax.text(3.5, 0.55, "시냅스 뒤 뉴런\n(수상돌기 가시)", ha="center", va="center", fontsize=9, color=C["green"])
ax.text(3.5, 4.2, "시냅스 앞 종말", ha="center", va="center", fontsize=9, color=C["blue"])
ax.text(5.65, 2.1, "틈\n약 20 nm", fontsize=8, va="center", ha="left")
ax.text(7.05, 3.55, "성상세포", ha="center", fontsize=8.5, color=C["gray"])
ax.text(7.05, 0.8, "글루탐산\n운반체", ha="center", va="top", fontsize=8, color=C["green"])
ax.text(3.5, -0.6, "활성대와 PSD 지름: 약 0.2–0.5 μm (크기 비율은 실제와 다르다)",
        ha="center", va="top", fontsize=8, color=C["gray"])

ax.set_xlim(-2.6, 7.7)
ax.set_ylim(-0.95, 5.1)
ax.set_aspect("equal")
ax.axis("off")
save(fig, __file__)
