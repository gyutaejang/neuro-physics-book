from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1, 1.05]))

# 왼쪽: 원자 장부. 반응 전과 후의 원자 수가 같다.
atoms = ["C", "H", "O"]
left = {"C": [("포도당", 6)], "H": [("포도당", 12)], "O": [("포도당", 6), ("O₂ 6개", 12)]}
right = {"C": [("CO₂ 6개", 6)], "H": [("H₂O 6개", 12)], "O": [("CO₂ 6개", 12), ("H₂O 6개", 6)]}
cols = {"포도당": C["green"], "O₂ 6개": C["blue"], "CO₂ 6개": C["gray"], "H₂O 6개": C["purple"]}
w = 0.36
for i, a in enumerate(atoms):
    for side, d, dx in (("전", left, -w / 2 - 0.02), ("후", right, w / 2 + 0.02)):
        bottom = 0
        for name, n in d[a]:
            a1.bar(i + dx, n, w, bottom=bottom, color=cols[name], alpha=0.8)
            bottom += n
        a1.text(i + dx, bottom + 0.4, f"{bottom}", ha="center", va="bottom", fontsize=8.5)
        a1.text(i + dx, -0.6, side, ha="center", va="top", fontsize=8, color=C["gray"])
a1.set_xticks(range(3))
a1.set_xticklabels(atoms, fontsize=10)
a1.tick_params(axis="x", pad=14, length=0)
a1.set_ylabel("원자 수")
a1.set_ylim(0, 21.5)
handles = [plt.Rectangle((0, 0), 1, 1, color=v, alpha=0.8) for v in cols.values()]
a1.legend(handles, list(cols.keys()), fontsize=7.5, loc="upper left", ncol=2)
a1.set_title("반응 전후의 원자 수", fontsize=10)

# 오른쪽: 산소-포도당 지수
labels = ["완전 산화\n(이론)", "휴지기 뇌\n(측정)", "강한 자극 중\n(일시적)"]
vals = [6.0, 5.5, 4.0]
colors = [C["gray"], C["blue"], C["red"]]
bars = a2.bar(range(3), vals, 0.55, color=colors, alpha=0.8)
for i, v in enumerate(vals):
    a2.text(i, v + 0.12, ("" if i == 0 else "약 ") + f"{v:g}", ha="center", va="bottom", fontsize=9)
a2.axhline(6, color=C["gray"], lw=0.8, ls=":")
a2.set_xticks(range(3))
a2.set_xticklabels(labels, fontsize=8.5)
a2.set_ylabel("O₂ 분자 수 / 포도당 1개")
a2.set_ylim(0, 7.2)
a2.set_title("산소-포도당 지수 (OGI)", fontsize=10)
fig.tight_layout()
save(fig, __file__)
