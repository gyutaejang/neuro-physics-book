from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(7.4, 3.5))
y0, y1 = 1.4, 2.6
ax.add_patch(Rectangle((-0.3, y0), 15.6, y1 - y0, color=C["green"], alpha=0.12, lw=0, zorder=0))
ax.plot([-0.3, 15.3], [y0, y0], color=C["green"], lw=0.8, alpha=0.6)
ax.plot([-0.3, 15.3], [y1, y1], color=C["green"], lw=0.8, alpha=0.6)
ax.text(-0.5, 3.4, "세포 밖", ha="right", va="center", fontsize=9)
ax.text(-0.5, 0.6, "세포 안", ha="right", va="center", fontsize=9)


def box(xc, w, col, label):
    ax.add_patch(FancyBboxPatch((xc - w / 2, y0 - 0.3), w, y1 - y0 + 0.6,
                                boxstyle="round,pad=0.05,rounding_size=0.3",
                                fc=col, ec="none", alpha=0.3, zorder=2))
    ax.text(xc, 4.55, label.replace("\n", " "), ha="center", va="bottom", fontsize=9, zorder=4, weight="bold")


def flux(x, up, text, col=C["green"], side="left"):
    ya, yb = (0.45, 3.55) if up else (3.55, 0.45)
    ax.annotate("", xy=(x, yb), xytext=(x, ya),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5, mutation_scale=11), zorder=5)
    ty = 3.85 if up else 3.85
    ax.text(x, 3.9, text, ha="center", va="bottom", fontsize=8.5, color=col)


specs = [
    (1.3, "Na⁺/K⁺\n펌프", C["red"], [(0.9, True, "3Na⁺"), (1.7, False, "2K⁺")], True,
     "ATP 1개\n기울기의 원천"),
    (4.4, "NKCC1", C["purple"], [(3.75, False, "Na⁺"), (4.4, False, "K⁺"), (5.05, False, "2Cl⁻")], False,
     "Cl⁻를 안으로\n(미성숙 뉴런)"),
    (7.5, "KCC2", C["purple"], [(7.15, True, "K⁺"), (7.85, True, "Cl⁻")], False,
     "Cl⁻를 밖으로\n(성숙 뉴런)"),
    (10.6, "NCX", C["purple"], [(10.1, False, "3Na⁺"), (11.1, True, "Ca²⁺")], False,
     "Na⁺ 기울기로\nCa²⁺ 퍼내기"),
    (13.7, "PMCA", C["red"], [(13.7, True, "Ca²⁺")], True,
     "ATP 1개\n높은 친화도"),
]
for xc, name, col, fl, atp, note in specs:
    box(xc, 1.9, col, name)
    for x, up, t in fl:
        flux(x, up, t, col=C["green"])
    ax.text(xc, -0.05, note, ha="center", va="top", fontsize=8,
            color=C["red"] if atp else C["purple"])

ax.text(1.3, -1.25, "1차 능동", ha="center", fontsize=8.5, color=C["red"], weight="bold")
ax.text(13.7, -1.25, "1차 능동", ha="center", fontsize=8.5, color=C["red"], weight="bold")
ax.text(7.5, -1.25, "2차 능동 (Na⁺ 또는 K⁺ 기울기를 쓴다)", ha="center", fontsize=8.5,
        color=C["purple"], weight="bold")
ax.set_xlim(-2.0, 15.3)
ax.set_ylim(-1.5, 5.0)
ax.axis("off")
save(fig, __file__)
