from figstyle import plt, np, save, C

# 폴링 전기음성도 (표준값)
en = [("K", 0.82), ("Na", 0.93), ("Mg", 1.31), ("P", 2.19), ("H", 2.20), ("C", 2.55),
      ("S", 2.58), ("N", 3.04), ("Cl", 3.16), ("O", 3.44), ("F", 3.98)]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.3))

names = [n for n, _ in en]
vals = [v for _, v in en]
cols = [C["green"] if n in ("K", "Na", "Mg") else (C["red"] if v >= 3.0 else C["blue"]) for n, v in en]
a1.bar(names, vals, color=cols, width=0.7)
for i, v in enumerate(vals):
    a1.text(i, v + 0.06, f"{v:.2f}", ha="center", va="bottom", fontsize=7)
a1.set_ylim(0, 4.6)
a1.set_ylabel("전기음성도 (폴링)")
a1.set_title("전자를 끌어당기는 정도", fontsize=10)
a1.text(-0.5, 2.75, "전자를 잘 내준다\n(양이온이 된다)", ha="left", fontsize=8, color=C["green"])
a1.text(8.6, 4.25, "전자를 세게 끈다", ha="center", fontsize=8, color=C["red"])

# 전기음성도 차이로 본 결합의 성격
bonds = [("C–C", 0.0), ("C–H", 0.35), ("N–H", 0.84), ("C–O", 0.89), ("O–H", 1.24),
         ("Na–Cl", 2.23), ("K–Cl", 2.34)]
a2.axvspan(0, 0.4, color=C["gray"], alpha=0.12, lw=0)
a2.axvspan(0.4, 1.8, color=C["blue"], alpha=0.12, lw=0)
a2.axvspan(1.8, 3.0, color=C["green"], alpha=0.14, lw=0)
a2.text(0.2, 1.75, "비극성\n공유", ha="center", va="top", fontsize=8.5)
a2.text(1.1, 1.75, "극성 공유", ha="center", va="top", fontsize=8.5, color=C["blue"])
a2.text(2.4, 1.75, "이온", ha="center", va="top", fontsize=8.5, color=C["green"])
pos = {"C–C": (1.3, "left"), "C–H": (0.75, "center"), "N–H": (0.35, "right"), "C–O": (1.1, "left"),
       "O–H": (0.55, "center"), "Na–Cl": (0.35, "right"), "K–Cl": (0.9, "left")}
for b, d in bonds:
    y, ha = pos[b]
    a2.plot([d, d], [0, y], color=C["gray"], lw=0.6)
    a2.plot(d, 0, "o", color=C["ink"], ms=4, zorder=3, clip_on=False)
    dx = {"left": 0.03, "right": -0.03, "center": 0}[ha]
    a2.text(d + dx, y, f"{b} {d:.2f}", ha=ha, va="bottom", fontsize=7.5)
a2.set_xlim(0, 3.0)
a2.set_ylim(0, 1.85)
a2.set_yticks([])
a2.spines["left"].set_visible(False)
a2.set_xlabel("두 원자의 전기음성도 차이")
a2.set_title("차이가 클수록 전자가 한쪽으로 쏠린다", fontsize=10)
save(fig, __file__)
