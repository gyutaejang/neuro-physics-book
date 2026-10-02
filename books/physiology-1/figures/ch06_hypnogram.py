from figstyle import plt, np, save, C

# 건강한 젊은 성인의 전형적인 하룻밤 (분 단위 모식). R = REM 수면
seq = [("W", 12), ("N1", 6), ("N2", 14), ("N3", 45), ("N2", 10), ("R", 8),
       ("N1", 2), ("N2", 25), ("N3", 32), ("N2", 14), ("R", 18), ("W", 2),
       ("N1", 4), ("N2", 38), ("N3", 13), ("N2", 16), ("R", 22), ("W", 3),
       ("N1", 4), ("N2", 52), ("R", 26), ("W", 3),
       ("N1", 6), ("N2", 67), ("R", 28), ("W", 10)]
level = {"W": 4, "R": 3, "N1": 2, "N2": 1, "N3": 0}
names = {4: "각성", 3: "REM", 2: "N1", 1: "N2", 0: "N3"}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw=dict(width_ratios=[3.2, 1]))
t0 = 0
xs, ys = [], []
for s, m in seq:
    y = level[s]
    xs += [t0 / 60, (t0 + m) / 60]
    ys += [y, y]
    if s == "R":
        a1.plot([t0 / 60, (t0 + m) / 60], [y, y], color=C["red"], lw=4, solid_capstyle="butt", zorder=3)
    if s == "N3":
        a1.plot([t0 / 60, (t0 + m) / 60], [y, y], color=C["blue"], lw=4, solid_capstyle="butt", zorder=3)
    t0 += m
a1.plot(xs, ys, color=C["ink"], lw=0.9)
a1.set_yticks(list(names))
a1.set_yticklabels([names[k] for k in names])
a1.set_ylim(-0.75, 4.8)
a1.set_xlim(0, 8)
a1.set_xlabel("잠자리에 든 뒤 시간 (h)")
a1.set_title("하룻밤 수면 단계도 (모식)", fontsize=10)
a1.text(0.5, -0.5, "N3는 밤의 앞쪽에", fontsize=8, color=C["blue"], ha="left", va="center")
a1.text(4.6, 4.5, "REM은 뒤로 갈수록 길어진다", fontsize=8, color=C["red"], ha="center", va="center")

tot = {}
for s, m in seq:
    tot[s] = tot.get(s, 0) + m
tst = sum(v for k, v in tot.items() if k != "W")
order = ["N1", "N2", "N3", "R"]
pct = [100 * tot[k] / tst for k in order]
cols = [C["gray"], C["gray"], C["blue"], C["red"]]
a2.barh(range(4), pct, color=cols, height=0.6)
for i, p in enumerate(pct):
    a2.text(p + 1.5, i, f"{p:.0f} %", va="center", fontsize=8)
a2.set_yticks(range(4))
a2.set_yticklabels(["N1", "N2", "N3", "REM"])
a2.invert_yaxis()
a2.set_xlim(0, 70)
a2.set_xlabel("총수면시간 대비 (%)")
a2.set_title(f"총수면 {tst / 60:.1f} h", fontsize=10)
fig.tight_layout()
save(fig, __file__)
