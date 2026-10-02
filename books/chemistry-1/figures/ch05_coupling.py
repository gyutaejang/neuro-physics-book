from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.2))


def waterfall(ax, steps, total_label, ylim):
    """steps: [(이름, ΔG, 색)]. 계단식으로 쌓고 합을 마지막 막대로 그린다."""
    y = 0
    for i, (name, d, col) in enumerate(steps):
        ax.bar(i, d, 0.55, bottom=y, color=col, alpha=0.8)
        ax.text(i, y + d + (1.2 if d > 0 else -1.2), f"{d:+.1f}".replace("-", "−"), ha="center",
                va="bottom" if d > 0 else "top", fontsize=8.5)
        if i < len(steps) - 1:
            ax.plot([i + 0.28, i + 0.72], [y + d, y + d], color=C["gray"], lw=0.7, ls=":")
        y += d
    k = len(steps)
    ax.bar(k, y, 0.55, color=C["red"], alpha=0.9)
    ax.text(k, y - 1.2, f"{y:+.1f}".replace("-", "−"), ha="center", va="top", fontsize=8.5, color=C["red"])
    ax.axhline(0, color=C["gray"], lw=0.8)
    ax.set_xticks(range(k + 1))
    ax.set_xticklabels([s[0] for s in steps] + [total_label], fontsize=8)
    ax.set_ylim(*ylim)
    ticks = [t for t in range(-60, 50, 20) if ylim[0] <= t <= ylim[1]]
    ax.set_yticks(ticks)
    ax.set_yticklabels([str(t).replace("-", "−") for t in ticks])


waterfall(a1, [("포도당 + Pᵢ\n→ 포도당-6-인산", 13.8, C["blue"]),
               ("ATP → ADP + Pᵢ\n(표준값)", -30.5, C["green"])], "짝지은 반응\n(헥소키나아제)", (-36, 22))
a1.set_ylabel("ΔG°′ (kJ/mol)")
a1.set_title("불리한 반응을 ATP로 끌기", fontsize=10)

waterfall(a2, [("Na⁺ 3개\n내보내기", 3 * 12.6, C["blue"]),
               ("K⁺ 2개\n들여오기", 2 * 1.84, C["blue"]),
               ("ATP 1개\n(세포 조건)", -52, C["green"])], "펌프 한 번\n합계", (-60, 50))
a2.set_ylabel("ΔG (kJ/mol)")
a2.set_title("Na⁺/K⁺ 펌프 (−70 mV, 37 °C)", fontsize=10)
fig.tight_layout()
save(fig, __file__)
