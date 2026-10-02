from figstyle import plt, np, save, C

RT = 8.314 * 310.15 / 1000
F = 96.485
V = -0.070
ions = [("Na⁺", 145, 15, 1), ("K⁺", 5, 140, 1), ("Ca²⁺", 1.5, 1e-4, 2), ("Cl⁻", 115, 8, -1)]
fig, ax = plt.subplots(figsize=(6.6, 3.2))
w = 0.26
for i, (n, co, ci, z) in enumerate(ions):
    ch = RT * np.log(ci / co)
    el = z * F * V
    tot = ch + el
    ax.bar(i - w, ch, w, color=C["green"], alpha=0.8, label="농도 몫  RT ln(c안/c밖)" if i == 0 else None)
    ax.bar(i, el, w, color=C["blue"], alpha=0.8, label="전기 몫  zFΔψ" if i == 0 else None)
    ax.bar(i + w, tot, w, color=C["red"], alpha=0.85, label="합: 전기화학 ΔG" if i == 0 else None)
    va = "top" if tot < 0 else "bottom"
    ax.text(i + w, tot + (-1 if tot < 0 else 1), f"{tot:+.1f}".replace("-", "−"), ha="center", va=va,
            fontsize=8, color=C["red"])
ax.axhline(0, color=C["gray"], lw=0.8)
ax.set_xticks(range(4))
ax.set_xticklabels([f"{n} 들어올 때" for n, *_ in ions])
ax.set_ylabel("이온 1 mol이 들어올 때의 ΔG (kJ/mol)", fontsize=9)
ax.set_ylim(-46, 16)
ax.set_yticks([-40, -30, -20, -10, 0, 10])
ax.set_yticklabels(["−40", "−30", "−20", "−10", "0", "10"])
ax.legend(fontsize=7.5, loc="lower right")
ax.text(-0.45, 12.5, "막전위 −70 mV, 37 °C. 음수 = 저절로 들어온다(내리막)", fontsize=8, color=C["gray"])
fig.tight_layout()
save(fig, __file__)
