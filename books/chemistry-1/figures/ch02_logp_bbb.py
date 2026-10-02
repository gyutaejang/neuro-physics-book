from figstyle import plt, np, save, C

# 실험 log P (옥탄올/물, 중성 분자 기준; PubChem 값). 경로: 수동 확산 / 운반체 / 거의 못 지남
mols = [
    ("글루탐산", -3.69, "no"), ("GABA", -3.17, "no"), ("포도당", -3.24, "tr"), ("L-DOPA", -2.39, "tr"),
    ("도파민", -0.98, "no"), ("에탄올", -0.31, "pd"), ("카페인", -0.07, "pd"), ("모르핀", 0.89, "pd"),
    ("니코틴", 1.17, "pd"), ("헤로인", 1.58, "pd"), ("디아제팜", 2.82, "pd"), ("프로포폴", 3.79, "pd"),
]
col = {"pd": C["blue"], "tr": C["green"], "no": C["red"]}
lab = {"pd": "지질막을 수동 확산으로 지난다", "tr": "운반체가 실어 나른다 (GLUT1, LAT1)", "no": "거의 지나지 못한다"}

fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.axvspan(1, 3, color=C["blue"], alpha=0.10, lw=0)
ax.text(2, 2.12, "중추신경계 약물이 흔히\n놓이는 범위 (대략)", ha="center", va="top", fontsize=8, color=C["blue"])
ax.axhline(0, color=C["gray"], lw=1)
levels = [0.55, -0.55, 1.0, -1.0]
for i, (n, v, k) in enumerate(sorted(mols, key=lambda m: m[1])):
    y = levels[i % 4]
    ax.plot([v, v], [0, y * 0.8], color=C["gray"], lw=0.6)
    ax.scatter([v], [0], s=36, color=col[k], zorder=3)
    ax.text(v, y, f"{n}\n{v:+.1f}".replace("-", "−"), ha="center", va="bottom" if y > 0 else "top", fontsize=8, color=col[k])
for k in ("pd", "tr", "no"):
    ax.scatter([], [], color=col[k], s=30, label=lab[k])
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=3, fontsize=8, handletextpad=0.3, columnspacing=1.2)
ax.set_xlim(-4.3, 4.3)
ax.set_ylim(-1.75, 2.15)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -1.75))
ax.set_xlabel("log P  (← 물을 좋아함 · 기름을 좋아함 →)")
save(fig, __file__)
