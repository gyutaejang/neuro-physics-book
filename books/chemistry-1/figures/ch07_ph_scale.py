from matplotlib.colors import LinearSegmentedColormap
from figstyle import plt, np, save, C

fig, ax = plt.subplots(figsize=(7.2, 3.4))
cmap = LinearSegmentedColormap.from_list("ph", [C["red"], "#f3f3f3", C["blue"]])
ax.imshow(np.linspace(0, 14, 400)[None, :], extent=(0, 14, -0.18, 0.18), cmap=cmap,
          aspect="auto", alpha=0.85, zorder=1)

# 몸 안 (위쪽): (pH, 이름, 글자 x, 글자 y)
body = [
    (1.5, "위액\n1–3", 1.5, 0.55),
    (4.7, "리소좀\n4.5–5", 4.6, 0.55),
    (5.6, "시냅스 소포\n약 5.6", 5.7, 1.05),
    (7.1, "세포 안\n7.0–7.2", 6.4, 1.6),
    (7.3, "뇌척수액\n약 7.3", 7.6, 1.05),
    (7.4, "혈액\n7.35–7.45", 8.6, 0.55),
]
for ph, name, tx, ty in body:
    ax.plot([ph, tx], [0.2, ty - 0.05], color=C["green"], lw=0.7, zorder=2)
    ax.scatter([ph], [0.2], s=14, color=C["green"], zorder=3)
    ax.text(tx, ty, name, ha="center", va="bottom", fontsize=8, color=C["ink"])

# 일상 (아래쪽)
daily = [(2.3, "레몬즙"), (5.0, "커피"), (8.1, "바닷물"), (12.5, "표백제")]
for ph, name in daily:
    ax.plot([ph, ph], [-0.2, -0.42], color=C["gray"], lw=0.7, zorder=2)
    ax.scatter([ph], [-0.2], s=14, color=C["gray"], zorder=3)
    ax.text(ph, -0.47, name, ha="center", va="top", fontsize=8, color=C["gray"])

ax.text(6.9, -1.0, "중성: 25 °C에서 pH 7.0, 37 °C에서 약 6.8", ha="center", va="top", fontsize=8,
        color=C["ink"])
ax.text(0.1, 0.24, "← 산성", ha="left", va="bottom", fontsize=9, color=C["red"])
ax.text(13.9, 0.24, "염기성 →", ha="right", va="bottom", fontsize=9, color=C["blue"])
ax.text(13.9, 1.95, "위 초록: 몸 안\n아래 회색: 일상", ha="right", va="top", fontsize=8, color=C["gray"])

ax.set_xlim(0, 14)
ax.set_ylim(-1.45, 2.1)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -1.45))
ax.set_xticks(range(0, 15, 1))
ax.set_xlabel("pH")
top = ax.secondary_xaxis("top")
top.set_xticks([0, 2, 4, 6, 7.4, 10, 12, 14])
top.set_xticklabels(["1 M", "10 mM", "100 μM", "1 μM", "40 nM", "0.1 nM", "1 pM", "10 fM"], fontsize=8)
top.set_xlabel("H⁺ 농도 (몰 농도)", fontsize=9)
save(fig, __file__)
