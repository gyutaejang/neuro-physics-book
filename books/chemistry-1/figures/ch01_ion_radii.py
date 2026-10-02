from figstyle import plt, np, save, C

# 이온 반지름 (Shannon, 배위수 6) / 수화 반지름 (Nightingale 1959), 단위 nm
ions = [("Li⁺", 0.076, 0.382), ("Na⁺", 0.102, 0.358), ("K⁺", 0.138, 0.331),
        ("Mg²⁺", 0.072, 0.428), ("Ca²⁺", 0.100, 0.412), ("Cl⁻", 0.181, 0.332)]
fig, ax = plt.subplots(figsize=(7.2, 3.0))
gap = 1.0
for i, (name, r, rh) in enumerate(ions):
    x = i * gap
    col = C["red"] if "⁻" in name else C["green"]
    ax.add_patch(plt.Circle((x, 0), rh, facecolor=C["light"], edgecolor=C["blue"], lw=0.8, ls="--"))
    ax.add_patch(plt.Circle((x, 0), r, facecolor=col, edgecolor="none", alpha=0.9))
    ax.text(x, 0.47, name, ha="center", va="bottom", fontsize=10.5)
    ax.text(x, -0.47, f"이온 {r:.3f} nm\n수화 {rh:.2f} nm", ha="center", va="top", fontsize=8)
ax.annotate("", xy=(2.0, 0.86), xytext=(0.0, 0.86), arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=0.9))
ax.text(1.0, 0.9, "맨 이온은 커지는데, 수화 이온은 작아진다", ha="center", va="bottom", fontsize=8, color=C["gray"])
ax.set_xlim(-0.55, (len(ions) - 1) * gap + 0.55)
ax.set_ylim(-0.85, 1.05)
ax.set_aspect("equal")
ax.axis("off")
h = [plt.Circle((0, 0), 1, facecolor=C["green"]), plt.Circle((0, 0), 1, facecolor=C["light"], edgecolor=C["blue"], ls="--")]
ax.legend(h, ["맨 이온 (결정 속 반지름)", "물 껍질까지 포함한 수화 이온"], loc="lower center",
          bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8)
save(fig, __file__)
