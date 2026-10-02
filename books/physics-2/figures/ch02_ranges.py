from figstyle import plt, np, save, C

# 물(연조직)에서 방사선이 들어가는 깊이. 하전 입자는 비정, 광자는 반가층.
items = [
    (0.04, "α 5 MeV\n비정 약 40 μm", C["red"]),
    (0.6, "¹⁸F 양전자\n평균 0.6 mm", C["red"]),
    (2.4, "¹⁸F 양전자\n최대 2.4 mm", C["red"]),
    (4.4, "전자 1 MeV\n비정 4.4 mm", C["red"]),
    (17, "⁸²Rb 양전자\n최대 약 17 mm", C["red"]),
    (45, "140 keV 광자\n반가층 4.5 cm", C["blue"]),
    (72, "511 keV 광자\n반가층 7.2 cm", C["blue"]),
]
refs = [(0.012, "세포 하나 약 10 μm"), (3, "피질 두께 2–4 mm"), (180, "머리 지름 약 18 cm")]
fig, ax = plt.subplots(figsize=(7.4, 3.4))
ax.set_xscale("log")
ax.set_xlim(5e-3, 400)
ax.set_ylim(-2.25, 1.9)
ax.axhline(0, color=C["gray"], lw=1.2, zorder=1)
lv = [0.45, -0.45, -1.15, 0.45, -0.45, 0.45, -1.15]
for (v, name, col), l in zip(items, lv):
    ax.plot([v, v], [0, l * 0.85], color=C["gray"], lw=0.6, zorder=1)
    ax.scatter([v], [0], s=30, color=col, zorder=3)
    ax.text(v, l, name, ha="center", va="bottom" if l > 0 else "top", fontsize=7.8, color=C["ink"])
ax.axvspan(2, 4, color=C["green"], alpha=0.12, lw=0, zorder=0)
for v, name in refs:
    ax.scatter([v], [0], s=40, marker="|", color=C["green"], zorder=3, lw=2)
    ax.text(v, -1.95, name.replace("\n", " "), ha="center", va="center", fontsize=7.6,
            color=C["green"])
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -2.25))
ax.set_xticks([0.01, 0.1, 1, 10, 100])
ax.set_xticklabels(["10 μm", "100 μm", "1 mm", "1 cm", "10 cm"])
ax.minorticks_off()
ax.set_xlabel("물(연조직) 속 깊이 (로그 눈금)")
ax.text(0.006, 1.6, "● 하전 입자: 비정 (여기서 멈춘다)", color=C["red"], fontsize=8)
ax.text(0.006, 1.3, "● 광자: 반가층 (절반이 남는다)", color=C["blue"], fontsize=8)
save(fig, __file__)
