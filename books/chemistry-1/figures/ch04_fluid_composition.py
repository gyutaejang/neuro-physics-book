from figstyle import plt, np, save, C

names = ["Na⁺", "K⁺", "Cl⁻", "HCO₃⁻", "Ca²⁺\n(이온화)", "Mg²⁺", "포도당"]
plasma = [140, 4.5, 103, 25, 1.2, 0.85, 5.0]
csf = [147, 2.9, 125, 23, 1.1, 1.2, 3.3]
icf = [15, 140, 8, 12, 1e-4, 0.5, 1.5]
groups = [("혈장", plasma, C["red"]), ("뇌척수액", csf, C["blue"]), ("뉴런 안 (자유 이온)", icf, C["green"])]

fig, ax = plt.subplots(figsize=(7.2, 3.4))
x = np.arange(len(names))
w = 0.26
for i, (lab, vals, col) in enumerate(groups):
    xs = x + (i - 1) * w
    ax.bar(xs, vals, width=w, color=col, alpha=0.85, label=lab, bottom=0)
    for xx, v in zip(xs, vals):
        s = "0.0001" if v < 1e-3 else (f"{v:.0f}" if v >= 10 else f"{v:g}")
        ax.text(xx, v * 1.15, s, ha="center", va="bottom", fontsize=6.8, color=C["ink"], rotation=90)
ax.set_yscale("log")
ax.set_ylim(5e-5, 2e3)
ax.set_yticks([1e-4, 1e-2, 1, 100])
ax.set_yticklabels(["0.0001", "0.01", "1", "100"])
ax.minorticks_off()
ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel("농도 (mM), 로그 눈금")
ax.legend(fontsize=8.5, loc="upper right", ncol=3, bbox_to_anchor=(1.0, 1.08))
save(fig, __file__)
