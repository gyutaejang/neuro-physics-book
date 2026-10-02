from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(7.2, 3.7))
ax.set_xlim(0, 10)
ax.set_ylim(0.25, 4.95)
ax.axis("off")


def box(x, y, text, col=C["blue"], w=1.75, h=0.78, fs=8.5, fill=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                facecolor=fill or "white", edgecolor=col, lw=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=C["ink"])


def arrow(p, q, col=C["blue"], ls="-", lw=1.4):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, ls=ls, mutation_scale=11,
                                shrinkA=0, shrinkB=0))


# 윗줄: 생성과 뇌실 경로
y1 = 4.15
xs = [1.0, 3.0, 5.0, 7.0, 9.0]
labels = ["맥락총\n(맥락얼기)", "측뇌실\n(좌우)", "제3뇌실", "제4뇌실", "지주막하 공간\n(뇌·척수 둘레)"]
for x, t in zip(xs, labels):
    box(x, y1, t, col=C["green"] if x == 1.0 else C["blue"],
        fill=C["light"] if x in (3.0, 5.0, 7.0) else None)
gaps = ["분비", "뇌실간공\n(먼로 구멍)", "중뇌수도관", "정중·외측구멍"]
for (a, b), g in zip(zip(xs[:-1], xs[1:]), gaps):
    arrow((a + 0.9, y1), (b - 0.9, y1))
    ax.text((a + b) / 2, y1 + 0.5, g, ha="center", va="bottom", fontsize=7.5, color=C["gray"])

ax.text(5.0, 3.35, "뇌실 전체 약 25 mL", ha="center", fontsize=8, color=C["blue"])
ax.text(1.0, 3.5, "약 0.35 mL/분\n(하루 약 500 mL)", ha="center", va="top", fontsize=8, color=C["green"])

# 아랫줄: 흡수 경로와 실질 교환
y2, ybus = 1.25, 2.55
outs = [(8.85, "지주막 과립\n→ 상시상정맥동", C["blue"], "-"),
        (6.45, "뇌신경·척수신경 뿌리\n사골판 → 림프", C["purple"], "-"),
        (4.05, "수막 림프관\n→ 목 림프절", C["purple"], "-"),
        (1.65, "뇌 실질\n(세포 사이 공간)", C["gray"], "--")]
ax.plot([9.0, 9.0], [y1 - 0.42, ybus], color=C["gray"], lw=1.2)
ax.plot([1.65, 9.0], [ybus, ybus], color=C["gray"], lw=1.2)
for x, t, col, ls in outs:
    box(x, y2, t, col=col, w=2.05, h=0.85, fs=8)
    arrow((x, ybus), (x, y2 + 0.45), col=col, ls=ls)
ax.text(9.1, 3.05, "흡수", ha="left", fontsize=8, color=C["gray"])
ax.text(5.25, 0.5, "림프 경로의 비중은 아직 연구 중", ha="center", fontsize=7.5, color=C["purple"])
ax.text(1.65, 0.5, "혈관 주위 공간으로\n드나드는 교환 (10.2절)", ha="center", va="center", fontsize=7.5, color=C["gray"])
ax.set_xlim(0.1, 9.95)
save(fig, __file__)
