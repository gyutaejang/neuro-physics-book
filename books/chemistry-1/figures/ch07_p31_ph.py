from figstyle import plt, np, save, C

PKA, D_HA, D_A = 6.77, 3.29, 5.68  # 무기인산 적정 상수 (PCr 기준 ppm)


def shift(ph):
    r = 10 ** (ph - PKA)
    return (D_HA + D_A * r) / (1 + r)


def lor(x, x0, w, a):
    return a * (w / 2) ** 2 / ((x - x0) ** 2 + (w / 2) ** 2)


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1.25, 1]))

x = np.linspace(-20, 10, 3000)
base = (lor(x, 6.8, 0.9, 0.35) + lor(x, 3.0, 1.0, 0.4) + lor(x, 0.0, 0.35, 1.0)
        + lor(x, -2.5, 0.6, 0.45) + lor(x, -7.6, 0.7, 0.42) + lor(x, -16.1, 0.8, 0.33))
d_norm, d_isch = shift(7.05), shift(6.4)
a1.plot(x, base + lor(x, d_norm, 0.45, 0.32), color=C["blue"], lw=1.2, label="정상 (pH 약 7.05)")
m = (x > 2.2) & (x < 6.0)
a1.plot(x[m], (base + lor(x, d_isch, 0.5, 0.45))[m], color=C["red"], lw=1.1, ls="--")
labels = [(6.8, "PME"), (d_norm, "Pi"), (3.0, "PDE"), (0.0, "PCr"), (-2.5, "γ-ATP"),
          (-7.6, "α-ATP"), (-16.1, "β-ATP")]
for pos, name in labels:
    top = base[np.argmin(abs(x - pos))] + (0.32 if name == "Pi" else 0)
    a1.text(pos, top + 0.05, name, ha="center", va="bottom", fontsize=7.5,
            color=C["blue"] if name == "Pi" else C["ink"])
a1.text(d_isch + 0.4, 0.9, "허혈 때 Pi\n(pH 약 6.4)", ha="center", va="bottom", fontsize=7.5, color=C["red"])
a1.annotate("", xy=(d_isch - 0.3, 0.8), xytext=(d_norm + 0.6, 0.8),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1, mutation_scale=9))
a1.set_xlim(10, -20)
a1.set_ylim(-0.05, 1.3)
a1.set_yticks([])
a1.spines["left"].set_visible(False)
a1.set_xlabel("화학적 이동 (ppm, PCr = 0)")
a1.set_title("³¹P 스펙트럼 (도식)", fontsize=9.5)

ph = np.linspace(5.5, 8.2, 300)
a2.plot(ph, shift(ph), color=C["blue"], lw=2)
a2.axhline(D_HA, color=C["gray"], lw=0.6, ls=":")
a2.axhline(D_A, color=C["gray"], lw=0.6, ls=":")
a2.text(5.55, D_A + 0.04, "HPO₄²⁻만 있을 때", ha="left", va="bottom", fontsize=7.5, color=C["gray"])
a2.text(8.2, D_HA + 0.04, "H₂PO₄⁻만 있을 때", ha="right", va="bottom", fontsize=7.5, color=C["gray"])
for p, col in ((7.05, C["blue"]), (6.4, C["red"])):
    a2.scatter([p], [shift(p)], color=col, s=22, zorder=5)
    a2.annotate(f"pH {p}: {shift(p):.2f} ppm", xy=(p, shift(p)), xytext=(10, -12), textcoords="offset points",
                fontsize=8, color=col)
a2.scatter([PKA], [shift(PKA)], color=C["ink"], s=14, zorder=5)
a2.annotate("pKa 6.77", xy=(PKA, shift(PKA)), xytext=(-48, 10), textcoords="offset points", fontsize=8)
a2.set_xlabel("pH")
a2.set_ylabel("Pi의 화학적 이동 (ppm)")
a2.set_title("Pi 이동으로 pH 읽기", fontsize=9.5)
a2.set_ylim(3.0, 6.0)
fig.tight_layout()
save(fig, __file__)
