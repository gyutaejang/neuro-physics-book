from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.4), gridspec_kw=dict(width_ratios=[1.05, 1]))

# 왼쪽: 양이온과 음이온 주변 물 분자의 방향 (도식)
def water(ax, cx, cy, h_angles, scale=0.25):
    """산소를 (cx, cy)에 두고 수소 두 개를 h_angles(라디안) 방향에 그린다."""
    for a in h_angles:
        hx, hy = cx + scale * np.cos(a), cy + scale * np.sin(a)
        ax.plot([cx, hx], [cy, hy], color=C["ink"], lw=1.2, zorder=2)
        ax.add_patch(plt.Circle((hx, hy), 0.09, facecolor="white", edgecolor=C["ink"], lw=0.7, zorder=3))
    ax.add_patch(plt.Circle((cx, cy), 0.14, facecolor=C["blue"], edgecolor=C["ink"], lw=0.7, zorder=3))

def ion(ax, x, y, r, label, col, n, anion):
    ax.add_patch(plt.Circle((x, y), r, facecolor=col, alpha=0.85, edgecolor=C["ink"], lw=0.8, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=10, color="white", zorder=4)
    R = r + (0.42 if anion else 0.2)
    hoh = np.deg2rad(104.5)
    for k in range(n):
        t = 2 * np.pi * k / n + 0.3
        cx, cy = x + R * np.cos(t), y + R * np.sin(t)
        if anion:   # 수소 하나가 이온을 곧바로 가리킨다 (O-H···Cl⁻)
            a0 = t + np.pi
            water(ax, cx, cy, (a0, a0 + hoh))
        else:       # 산소가 이온 쪽, 수소 둘은 바깥으로 벌어진다
            water(ax, cx, cy, (t + hoh / 2, t - hoh / 2))

ion(a1, 0, 0, 0.30, "Na⁺", C["green"], 6, False)
ion(a1, 2.85, 0, 0.55, "Cl⁻", C["red"], 6, True)
a1.text(0, -1.35, "산소(δ−)가 안쪽", ha="center", fontsize=8.5)
a1.text(2.85, -1.55, "수소(δ+)가 안쪽", ha="center", fontsize=8.5)
a1.set_xlim(-1.3, 4.2)
a1.set_ylim(-1.8, 1.5)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 수화 자유에너지 실험값(Marcus 1991)과 본 모형
k_na = 138.9  # N_A e^2 / (4 pi eps0), kJ·nm/mol
r = np.linspace(0.055, 0.18, 200)
for z, col in ((1, C["blue"]), (2, C["purple"])):
    born = z**2 * k_na / (2 * (r + 0.085)) * (1 - 1 / 80)
    a2.plot(r, born, color=col, lw=1, ls="--")
ions = [("Li⁺", 0.076, 475, 1), ("Na⁺", 0.102, 365, 1), ("K⁺", 0.138, 295, 1), ("Rb⁺", 0.152, 275, 1),
        ("Cs⁺", 0.167, 250, 1), ("Mg²⁺", 0.072, 1830, 2), ("Ca²⁺", 0.100, 1505, 2), ("Sr²⁺", 0.118, 1380, 2)]
for name, ri, g, z in ions:
    col = C["blue"] if z == 1 else C["purple"]
    a2.scatter([ri], [g], color=col, s=24, zorder=4)
    a2.annotate(name, xy=(ri, g), xytext=(4, 5), textcoords="offset points", fontsize=8.5)
a2.set_yscale("log")
a2.set_ylim(180, 3000)
a2.set_yticks([200, 300, 500, 1000, 2000])
a2.set_yticklabels(["200", "300", "500", "1000", "2000"])
a2.minorticks_off()
a2.set_xlim(0.05, 0.19)
a2.set_xlabel("맨 이온의 반지름 (nm)")
a2.set_ylabel("수화 에너지 크기 (kJ/mol)")
a2.text(0.123, 650, "본 모형 (점선)", fontsize=8.5, color=C["gray"])
a2.text(0.15, 1750, "2가", fontsize=9, color=C["purple"])
a2.text(0.17, 320, "1가", fontsize=9, color=C["blue"])
fig.tight_layout()
save(fig, __file__)
