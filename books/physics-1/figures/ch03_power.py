from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1.7, 1]})

rows = [
    ("뉴런 하나 (평균)", 2e-10, C["green"]),
    ("LED 전구", 10, C["gray"]),
    ("사람 뇌", 20, C["green"]),
    ("안정 시 몸 전체", 100, C["green"]),
    ("계단 뛰어오르기\n(역학적 일률)", 180, C["red"]),
    ("전기 주전자", 2000, C["gray"]),
]
y = np.arange(len(rows))[::-1]
for yi, (name, p, col) in zip(y, rows):
    a1.barh(yi, p, left=1e-11, color=col, alpha=0.75, height=0.6)
    lab = "0.2 nW" if p < 1 else (f"{p/1000:g} kW" if p >= 1000 else f"{p:g} W")
    a1.text(p * 1.6, yi, lab, va="center", fontsize=8.5)
a1.set_xscale("log")
a1.set_xlim(1e-11, 1e5)
a1.set_yticks(y)
a1.set_yticklabels([r[0] for r in rows], fontsize=8.5)
a1.set_xticks([1e-9, 1e-6, 1e-3, 1, 1e3])
a1.set_xticklabels(["1 nW", "1 μW", "1 mW", "1 W", "1 kW"], fontsize=8)
a1.minorticks_off()
a1.set_xlabel("일률 (W, 로그 눈금)")
a1.set_title("일률의 크기 지도")

cats = ["몸무게", "안정 대사\n에너지"]
vals = [2, 20]
a2.bar(cats, [100, 100], color=C["light"], width=0.55)
a2.bar(cats, vals, color=C["green"], width=0.55, alpha=0.85)
for i, v in enumerate(vals):
    a2.text(i, v + 3, f"뇌 {v}%", ha="center", va="bottom", fontsize=9, color=C["green"], weight="bold")
a2.set_ylim(0, 105)
a2.set_ylabel("몸 전체에 대한 비율 (%)")
a2.set_title("뇌가 차지하는 몫")
a2.tick_params(axis="x", labelsize=8.5)
fig.tight_layout()
save(fig, __file__)
