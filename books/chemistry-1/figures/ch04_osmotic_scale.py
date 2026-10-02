from figstyle import plt, np, save, C

f = 19.3  # mmHg per mOsm/L at 37 °C
rows = [
    ("정상 두개내압", 10, "mech"),
    ("삼투 농도 1 mOsm/L 차이", 1 * f, "osm"),
    ("혈장 콜로이드 삼투압 (단백질)", 25, "osm"),
    ("평균 동맥압", 90, "mech"),
    ("혈장 Na⁺ 5 mM 차이 (≈10 mOsm/L)", 10 * f, "osm"),
    ("체액 전체의 삼투압 (290 mOsm/L)", 290 * f, "osm"),
]
fig, ax = plt.subplots(figsize=(6.8, 2.9))
y = np.arange(len(rows))[::-1]
for yy, (lab, v, kind) in zip(y, rows):
    col = C["blue"] if kind == "osm" else C["gray"]
    ax.barh(yy, v, color=col, alpha=0.85, height=0.6)
    ax.text(v * 1.12, yy, f"약 {float(f'{v:.2g}'):,.0f} mmHg", va="center", fontsize=8.5)
ax.set_yticks(y)
ax.set_yticklabels([r[0] for r in rows], fontsize=9)
ax.set_xscale("log")
ax.set_xlim(1, 3e4)
ax.set_xticks([1, 10, 100, 1000, 10000])
ax.set_xticklabels(["1", "10", "100", "1000", "10⁴"])
ax.minorticks_off()
ax.set_xlabel("압력 (mmHg), 로그 눈금")
ax.text(1.2, -0.95, "파랑: 삼투압 (π = cRT, 37 °C)   회색: 기계적 압력", fontsize=8, color=C["gray"])
ax.set_ylim(-1.2, len(rows) - 0.5)
save(fig, __file__)
