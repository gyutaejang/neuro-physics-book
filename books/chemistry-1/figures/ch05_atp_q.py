from figstyle import plt, np, save, C

RT = 8.314 * 310.15 / 1000  # kJ/mol
dG0 = -30.5
logQ = np.linspace(-6, 6.5, 300)
dG = dG0 + RT * np.log(10) * logQ
fig, ax = plt.subplots(figsize=(6.4, 3.1))
ax.plot(logQ, dG, color=C["blue"], lw=2)
ax.axhline(0, color=C["gray"], lw=0.7)
ax.axvline(0, color=C["gray"], lw=0.6, ls=":")

pts = [
    (0, dG0, "표준 조건 (Q = 1)\nΔG° = −30.5", (0.8, -46)),
    (np.log10(2e-4), dG0 + RT * np.log(2e-4), "세포 안\n(ATP 3, ADP 0.3, Pᵢ 2 mM)\nΔG ≈ −52", (-5.8, -30)),
    (np.log10(np.exp(-dG0 / RT)), 0, "평형 (Q = K ≈ 1.4×10⁵)\nΔG = 0", (2.2, 9)),
]
for x, y, t, (tx, ty) in pts:
    ax.scatter([x], [y], color=C["red"], s=26, zorder=4)
    ax.annotate(t.replace("-", "−"), xy=(x, y), xytext=(tx, ty), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.7))
ax.text(-5.8, 3.5, "ΔG > 0: ATP가 합성되는 쪽", fontsize=8, color=C["gray"])
ax.text(3.6, -62, "ΔG < 0: 가수분해가\n저절로 일어나는 쪽", fontsize=8, color=C["gray"])
ax.set_xlabel("log₁₀ Q,   Q = [ADP][Pᵢ] / [ATP]  (농도는 M 단위)")
ax.set_ylabel("ΔG (kJ/mol)")
ax.set_xticks(range(-6, 7, 2))
ax.set_xticklabels([str(t).replace("-", "−") for t in range(-6, 7, 2)])
ax.set_ylim(-68, 20)
ax.set_yticks([-60, -40, -20, 0, 20])
ax.set_yticklabels(["−60", "−40", "−20", "0", "20"])
ax.text(4.3, -18, "Q가 10배 → ΔG 약 5.9 kJ/mol", fontsize=8, color=C["blue"], rotation=0)
fig.tight_layout()
save(fig, __file__)
