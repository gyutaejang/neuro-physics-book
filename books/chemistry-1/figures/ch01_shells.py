from figstyle import plt, np, save, C

atoms = [("H", "수소", 1, [1]), ("C", "탄소", 6, [2, 4]), ("O", "산소", 8, [2, 6]),
         ("Na", "나트륨", 11, [2, 8, 1]), ("Cl", "염소", 17, [2, 8, 7]), ("K", "칼륨", 19, [2, 8, 8, 1])]
fig, axes = plt.subplots(2, 3, figsize=(6.6, 4.5))
for ax, (sym, name, Z, shells) in zip(axes.flat, atoms):
    radii = [0.42 + 0.3 * i for i in range(4)]
    for i, n in enumerate(shells):
        R = radii[i]
        ax.add_patch(plt.Circle((0, 0), R, fill=False, color=C["gray"], lw=0.7))
        last = i == len(shells) - 1
        col = C["red"] if last else C["blue"]
        for k in range(n):
            a = np.pi / 2 + 2 * np.pi * k / n + (0.25 if i % 2 else 0)
            ax.add_patch(plt.Circle((R * np.cos(a), R * np.sin(a)), 0.065, color=col, zorder=3))
    ax.add_patch(plt.Circle((0, 0), 0.2, color=C["ink"], zorder=3))
    ax.text(0, 0, f"+{Z}", ha="center", va="center", color="white", fontsize=7.5, zorder=4)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.75, 1.45)
    ax.set_aspect("equal")
    ax.axis("off")
    cfg = "–".join(str(n) for n in shells)
    ax.set_title(f"{name} {sym}  ({cfg})", fontsize=10)
    v = shells[-1]
    ax.text(0, -1.6, f"원자가 전자 {v}개", ha="center", va="bottom", fontsize=9, color=C["red"])
fig.tight_layout(h_pad=0.6)
save(fig, __file__)
