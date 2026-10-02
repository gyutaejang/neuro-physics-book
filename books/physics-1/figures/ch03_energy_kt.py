from figstyle import plt, np, save, C

rows = [
    ("열에너지 kT (37 °C)", 1.0, C["gray"]),
    ("Na⁺ 하나가 70 mV를 넘을 때", 2.6, C["green"]),
    ("물속 수소 결합 하나", 3.0, C["blue"]),
    ("Na⁺/K⁺ 펌프 한 회 (3 Na⁺ + 2 K⁺)", 16, C["green"]),
    ("ATP 하나의 가수분해 (세포 조건)", 20, C["red"]),
    ("탄소-탄소 공유 결합", 135, C["blue"]),
]
fig, ax = plt.subplots(figsize=(6.6, 2.9))
y = np.arange(len(rows))[::-1]
for yi, (name, v, col) in zip(y, rows):
    ax.barh(yi, v, left=0.5, color=col, alpha=0.75, height=0.6)
    txt = f"약 {v:g} kT" if v != 1 else "1 kT"
    if name.startswith("물속"):
        txt = "수 kT"
    ax.text(v * 1.15 + 0.5, yi, txt, va="center", fontsize=8.5)
ax.set_xscale("log")
ax.set_xlim(0.5, 600)
ax.set_yticks(y)
ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
ax.set_xticks([1, 10, 100])
ax.set_xticklabels(["1", "10", "100"])
ax.minorticks_off()
ax.axvline(1, color=C["gray"], lw=0.8, ls=":")
ax.set_xlabel("에너지 (kT의 몇 배인가, 로그 눈금)")
fig.tight_layout()
save(fig, __file__)
