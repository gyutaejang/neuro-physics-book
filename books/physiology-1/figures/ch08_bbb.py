from figstyle import plt, np, save, C
from matplotlib.patches import Circle, Wedge, Ellipse, FancyBboxPatch

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.5), gridspec_kw=dict(width_ratios=[1, 1.15]))

# 왼쪽: 모세혈관 단면
a1.add_patch(Circle((0, 0), 2.15, fc=C["green"], alpha=0.25, ec=C["green"], lw=1))     # 성상세포 종족
for th in (40, 130, 220, 310):
    a1.plot([1.85 * np.cos(np.radians(th)), 2.15 * np.cos(np.radians(th))],
            [1.85 * np.sin(np.radians(th)), 2.15 * np.sin(np.radians(th))], color="white", lw=1.5)
a1.add_patch(Circle((0, 0), 1.85, fc="white", ec=C["gray"], lw=1.2))                  # 기저막
a1.add_patch(Wedge((0, 0), 1.80, 200, 300, width=0.32, fc=C["purple"], alpha=0.55, ec="none"))  # 주피세포
a1.add_patch(Circle((0, 0), 1.45, fc="#f3e3d3", ec=C["red"], lw=1))                   # 내피
a1.add_patch(Circle((0, 0), 1.0, fc="white", ec=C["red"], lw=1))                      # 내강
a1.add_patch(Ellipse((0.05, 0.05), 1.3, 0.85, fc=C["red"], alpha=0.75, ec="none"))   # 적혈구
for th in (75, 255):
    x0, y0 = 1.0 * np.cos(np.radians(th)), 1.0 * np.sin(np.radians(th))
    x1, y1 = 1.45 * np.cos(np.radians(th)), 1.45 * np.sin(np.radians(th))
    a1.plot([x0, x1], [y0, y1], color=C["ink"], lw=3.2)
kw = dict(fontsize=8, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a1.annotate("적혈구 (지름 약 7 μm)", xy=(0.3, 0.1), xytext=(-2.9, 3.0), **kw)
a1.annotate("내피세포", xy=(-1.2, 0.4), xytext=(-3.2, 1.5), **kw)
a1.annotate("밀착 연접", xy=(0.31, 1.25), xytext=(0.9, 2.95), **kw)
a1.annotate("기저막", xy=(1.3, -1.3), xytext=(2.0, -2.75), **kw)
a1.annotate("주피세포", xy=(-0.9, -1.4), xytext=(-3.2, -2.5), **kw)
a1.annotate("성상세포 종족", xy=(1.75, 1.0), xytext=(2.0, 2.3), **kw)
a1.set_xlim(-3.3, 3.6)
a1.set_ylim(-3.1, 3.4)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("뇌 모세혈관 단면 (도식)", fontsize=10)

# 오른쪽: 장벽을 건너는 길
a2.add_patch(FancyBboxPatch((0, 1.6), 10, 0.9, boxstyle="round,pad=0.02", fc="#f3e3d3", ec=C["red"], lw=0.8))
a2.text(0.1, 3.75, "혈액", fontsize=8.5, color=C["red"])
a2.text(0.1, 0.05, "뇌 (세포 사이 공간)", fontsize=8.5, color=C["green"])
a2.text(10.0, 1.5, "내피세포", fontsize=7.5, color=C["red"], ha="right", va="top")
items = [
    (0.9, "down", C["blue"], "O$_2$, CO$_2$\n지용성 약물", "막을 직접"),
    (2.9, "down", C["green"], "포도당", "GLUT1"),
    (4.6, "down", C["green"], "큰 중성\n아미노산", "LAT1"),
    (6.3, "down", C["green"], "젖산\n케톤체", "MCT1"),
    (7.9, "up", C["purple"], "일부 약물", "P-gp\n(내보냄)"),
    (9.3, "block", C["red"], "Gd 조영제\n알부민", "막힘"),
]
for x, kind, col, lab, tr in items:
    if kind == "down":
        a2.annotate("", xy=(x, 0.9), xytext=(x, 3.2),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6, mutation_scale=11))
    elif kind == "up":
        a2.annotate("", xy=(x, 3.2), xytext=(x, 0.9),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6, mutation_scale=11))
    else:
        a2.annotate("", xy=(x, 2.55), xytext=(x, 3.2),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6, mutation_scale=11))
        a2.text(x, 2.05, "×", color=col, fontsize=15, ha="center", va="center")
    a2.text(x, 3.3, lab, ha="center", va="bottom", fontsize=7.5)
    if kind != "block":
        a2.text(x, 0.8, tr, ha="center", va="top", fontsize=7.3, color=col)
a2.set_xlim(-0.2, 10.2)
a2.set_ylim(-0.4, 4.5)
a2.axis("off")
a2.set_title("장벽을 건너는 길", fontsize=10)
fig.tight_layout()
save(fig, __file__)
