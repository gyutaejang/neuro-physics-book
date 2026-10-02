from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1, 1.15]))

# 왼쪽: 시각 자극 중 증가율(%). Fox 외(1988)와 후속 연구의 흔한 범위.
names = ["혈류\n(CBF)", "포도당\n(CMRglc)", "산소\n(CMRO₂)"]
fox = [50, 51, 5]
lo = [30, 20, 10]
hi = [50, 50, 20]
cols = [C["blue"], C["green"], C["red"]]
x = np.arange(3)
a1.bar(x - 0.18, fox, 0.34, color=cols, alpha=0.85)
for i in range(3):
    a1.text(i - 0.18, fox[i] + 1.5, f"{fox[i]}", ha="center", va="bottom", fontsize=8)
    a1.plot([i + 0.18] * 2, [lo[i], hi[i]], color=cols[i], lw=6, alpha=0.4, solid_capstyle="butt")
a1.set_xticks(x)
a1.set_xticklabels(["혈류\n(CBF)", "포도당\n(CMRglc)", "산소\n(CMRO$_2$)"], fontsize=8.5)
a1.set_ylabel("자극 중 증가 (%)")
a1.set_ylim(0, 62)

# 오른쪽: 산소-포도당 지수. 휴지기, 활성 중 전체, 늘어난 몫만
base = 5.5
sc = [("Fox 외 (1988): CMRglc +51%, CMRO$_2$ +5%", 0.51, 0.05), ("CMRglc +30%, CMRO$_2$ +15%", 0.30, 0.15)]
labels = ["휴지기", "활성 중\n전체", "늘어난\n몫만"]
w = 0.36
for j, (name, dg, do) in enumerate(sc):
    vals = [base, base * (1 + do) / (1 + dg), base * do / dg]
    xs = np.arange(3) + (j - 0.5) * w
    a2.bar(xs, vals, w, color=C["blue"] if j == 0 else C["purple"], alpha=0.8 if j == 0 else 0.55,
           label=name)
    for xx, v in zip(xs, vals):
        a2.text(xx, v + 0.1, f"{v:.1f}", ha="center", va="bottom", fontsize=7.8)
a2.axhline(6, color=C["gray"], lw=0.8, ls=":")
a2.text(-0.45, 6.05, "완전 산화 6", ha="left", va="bottom", fontsize=7.6, color=C["gray"])
a2.set_xticks(range(3))
a2.set_xticklabels(labels, fontsize=8.5)
a2.set_ylabel("OGI (O$_2$ / 포도당)")
a2.set_ylim(0, 8.4)
a2.legend(fontsize=7.4, loc="upper right")
fig.tight_layout(w_pad=2.5)
save(fig, __file__)
