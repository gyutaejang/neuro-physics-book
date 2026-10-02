from figstyle import plt, np, save, C
from matplotlib.patches import Polygon, Rectangle

rng = np.random.default_rng(4)
fig, ax = plt.subplots(figsize=(7.0, 3.9))

# 층 경계 (위가 연질막, 아래가 백질). 전체 두께 약 2.5 mm로 그린다.
layers = [("1", 0.25, 25, 1.0), ("2/3", 0.75, 900, 1.4), ("4", 0.30, 1100, 1.0),
          ("5", 0.50, 380, 2.2), ("6", 0.55, 600, 1.4)]
top = 0.0
X0, X1 = 0.0, 2.2
bounds = []
for name, th, n, sz in layers:
    y0, y1 = top - th, top
    xs = rng.uniform(X0 + 0.05, X1 - 0.05, n)
    ys = rng.uniform(y0 + 0.02, y1 - 0.02, n)
    ss = sz * rng.uniform(0.6, 1.6, n)
    ax.scatter(xs, ys, s=ss, color=C["purple"], alpha=0.75, lw=0)
    if name == "5":   # 큰 피라미드 세포체 몇 개
        for xx in rng.uniform(0.2, 2.0, 6):
            yy = rng.uniform(y0 + 0.1, y1 - 0.1)
            ax.add_patch(Polygon([(xx, yy + 0.05), (xx - 0.035, yy - 0.03), (xx + 0.035, yy - 0.03)],
                                 fc=C["purple"], ec="none", alpha=0.85))
    ax.text(X0 - 0.12, (y0 + y1) / 2, f"{name}층", ha="right", va="center", fontsize=9)
    ax.plot([X0 - 0.05, X1 + 0.05], [y0, y0], color=C["gray"], lw=0.6, ls="--")
    bounds.append((name, y0, y1))
    top = y0
bottom = top
ax.add_patch(Rectangle((X0, bottom - 0.35), X1 - X0, 0.35, fc="#f0f0f0", ec="none"))
ax.text((X0 + X1) / 2, bottom - 0.18, "백질 (축삭과 수초)", ha="center", va="center", fontsize=8.5, color=C["gray"])
ax.plot([X0 - 0.05, X1 + 0.05], [0, 0], color=C["ink"], lw=1.2)
ax.text((X0 + X1) / 2, 0.05, "연질막 (뇌 표면)", ha="center", va="bottom", fontsize=8.5)
# 두께 자
ax.annotate("", xy=(-0.75, 0), xytext=(-0.75, bottom), arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8))
ax.text(-0.82, bottom / 2, "약 2–4 mm", rotation=90, ha="right", va="center", fontsize=8.5)
ax.text((X0 + X1) / 2, bottom - 0.45, "니슬 염색처럼 그린 세포체 분포 (도식)", ha="center", va="top", fontsize=7.8, color=C["gray"])

# 5층 피라미드 뉴런 하나: 꼭대기 수상돌기가 1층까지
px = 1.9
y5 = [b for b in bounds if b[0] == "5"][0]
sy = (y5[1] + y5[2]) / 2
ax.add_patch(Polygon([(px, sy + 0.09), (px - 0.07, sy - 0.05), (px + 0.07, sy - 0.05)], fc="#dcebd8", ec=C["green"], lw=1.2, zorder=3))
ax.plot([px, px], [sy + 0.09, -0.1], color=C["green"], lw=2.0, zorder=3)
for a in (0.6, 1.2, 1.9, 2.5):
    ax.plot([px, px + 0.25 * np.cos(a)], [-0.1, -0.1 + 0.08 * np.sin(a) - 0.0], color=C["green"], lw=1.3, zorder=3)
for a in (-0.4, -1.2, -1.9, -2.7):
    ax.plot([px, px + 0.2 * np.cos(a)], [sy - 0.05, sy - 0.05 + 0.15 * np.sin(a)], color=C["green"], lw=1.3, zorder=3)
ax.plot([px, px], [sy - 0.05, bottom - 0.3], color=C["red"], lw=1.3, zorder=3)


# 입출력 화살표 (오른쪽)
ARX = 3.2


def arrow(y, text, left=True, col=C["blue"]):
    if left:
        ax.annotate("", xy=(X1 + 0.08, y), xytext=(ARX, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.3, mutation_scale=10))
    else:
        ax.annotate("", xy=(ARX, y), xytext=(X1 + 0.08, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.3, mutation_scale=10))
    ax.text(ARX + 0.08, y, text, va="center", fontsize=8.2, color=col)


yc = {b[0]: (b[1] + b[2]) / 2 for b in bounds}
arrow(yc["2/3"], "다른 피질 영역 (피질-피질 연결)", left=False, col=C["red"])
arrow(yc["4"], "시상에서 오는 감각 입력", left=True, col=C["blue"])
arrow(yc["5"] - 0.1, "선조체, 뇌간, 척수 (피질하 출력)", left=False, col=C["red"])
arrow(yc["6"], "시상으로 되먹임", left=False, col=C["red"])
ax.set_xlim(-1.2, 6.1)
ax.set_ylim(bottom - 0.65, 0.25)
ax.axis("off")
save(fig, __file__)
