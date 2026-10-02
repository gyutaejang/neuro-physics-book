from figstyle import plt, np, save, C

fig, ax = plt.subplots(figsize=(6.6, 3.3))
pH = np.linspace(1, 13, 400)
acids = [("젖산", 3.86, C["red"]), ("인산 (H₂PO₄⁻/HPO₄²⁻)", 6.8, C["blue"]),
         ("암모늄 (NH₄⁺/NH₃)", 9.25, C["purple"])]
for name, pka, col in acids:
    frac = 1 / (1 + 10 ** (pka - pH))
    ax.plot(pH, frac * 100, color=col, lw=1.6, label=f"{name}, pKa {pka}")
    ax.scatter([pka], [50], color=col, s=18, zorder=4)
    f74 = 100 / (1 + 10 ** (pka - 7.4))
    ax.scatter([7.4], [f74], color=col, s=22, zorder=4, marker="D")
ax.axvline(7.4, color=C["green"], lw=1, ls="--")
ax.text(7.5, 104, "혈액 pH 7.4", color=C["green"], fontsize=8.5, va="bottom")
ax.axhline(50, color=C["gray"], lw=0.6, ls=":")
ax.annotate("pH = pKa에서\n정확히 절반", xy=(3.86, 50), xytext=(1.3, 70), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.7))
ax.annotate("99.97%", xy=(7.4, 99.97), xytext=(8.1, 90), fontsize=8, color=C["red"],
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.5))
ax.annotate("80%", xy=(7.4, 79.9), xytext=(8.1, 72), fontsize=8, color=C["blue"],
            arrowprops=dict(arrowstyle="-", color=C["blue"], lw=0.5))
ax.annotate("1.4%", xy=(7.4, 1.4), xytext=(5.5, 12), fontsize=8, color=C["purple"],
            arrowprops=dict(arrowstyle="-", color=C["purple"], lw=0.5))
ax.set_xlim(1, 13)
ax.set_ylim(-3, 112)
ax.set_xlabel("pH")
ax.set_ylabel("양성자를 내준 꼴의 비율 (%)")
ax.set_yticks([0, 25, 50, 75, 100])
ax.legend(fontsize=8, loc="lower right")
save(fig, __file__)
