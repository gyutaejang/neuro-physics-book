from figstyle import plt, np, save, C

# 유효선량의 크기 지도 (mSv, 로그 눈금). 값은 성인 기준의 대표값이다.
items = [
    (0.005, "치과 X선\n약 0.005", C["blue"]),
    (0.02, "흉부 X선\n약 0.02", C["blue"]),
    (0.1, "장거리 왕복 비행\n약 0.1", C["gray"]),
    (2, "머리 CT\n약 2", C["blue"]),
    (3, "자연 방사선 1년\n약 3", C["gray"]),
    (6.5, "FDG·아밀로이드 PET\n약 5–7", C["red"]),
    (20, "방사선 작업 종사자\n연간 한도 20", C["gray"]),
    (100, "위험 증가가 역학으로\n보이기 시작 약 100", C["gray"]),
    (1000, "급성 방사선 증상\n약 1000 (1 Sv)", C["gray"]),
]
fig, ax = plt.subplots(figsize=(7.4, 3.2))
ax.set_xscale("log")
ax.set_xlim(2e-3, 4000)
ax.set_ylim(-1.75, 1.75)
ax.axhline(0, color=C["gray"], lw=1.2, zorder=1)
lv = [0.5, -0.5, 0.5, -0.5, 0.5, -1.15, 1.15, -0.5, 0.5]
for (v, name, col), l in zip(items, lv):
    ax.plot([v, v], [0, l * 0.85], color=C["gray"], lw=0.6, zorder=1)
    ax.scatter([v], [0], s=30, color=col, zorder=3)
    ax.text(v, l, name, ha="center", va="bottom" if l > 0 else "top", fontsize=7.8)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -1.75))
ax.set_xticks([0.01, 0.1, 1, 10, 100, 1000])
ax.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
ax.minorticks_off()
ax.set_xlabel("유효선량 (mSv, 로그 눈금)")
ax.text(0.0025, 1.6, "● 의료 검사", color=C["blue"], fontsize=8)
ax.text(0.0025, 1.35, "● 뇌 PET", color=C["red"], fontsize=8)
ax.text(0.0025, 1.1, "● 비교 기준", color=C["gray"], fontsize=8)
save(fig, __file__)
