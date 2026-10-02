from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0))
x = np.linspace(0, 5, 300)
a1.plot(x, np.exp(-x), color=C["blue"], lw=1.8)
for n in (1, 2, 3):
    a1.plot([n, n], [0, np.exp(-n)], color=C["gray"], lw=0.6, ls=":")
    a1.text(n + 0.08, np.exp(-n) + 0.03, f"{np.exp(-n):.2f}", fontsize=8.5)
a1.set_xlabel("에너지 차이 ΔE (kT 단위)")
a1.set_ylabel("상대 확률 $e^{-\\Delta E/kT}$")
a1.set_title("선형 눈금: kT마다 약 1/e배")
a1.set_xlim(0, 5)
a1.set_ylim(0, 1.05)

kT = 0.02673  # eV, 37 °C
x2 = np.linspace(0, 45, 300)
a2.semilogy(x2, np.exp(-x2), color=C["blue"], lw=1.8)
marks = [(kT, "열에너지 kT = 0.027 eV", (8, 0.3)),
         (0.07, "막전위를 넘는 이온\n0.07 eV (2.6 kT)", (12, 1e-3)),
         (0.52, "ATP 하나\n0.5 eV (19 kT)", (24, 1e-8)),
         (1.0, "1 eV (37 kT)", (22, 1e-18))]
for E, lab, pos in marks:
    xx = E / kT
    yy = np.exp(-xx)
    a2.scatter([xx], [yy], color=C["red"], s=22, zorder=3)
    a2.annotate(lab, xy=(xx, yy), xytext=pos, fontsize=8, va="center",
                arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.set_xlabel("에너지 차이 ΔE (kT 단위)")
a2.set_title("로그 눈금: 직선으로 떨어진다")
a2.set_ylim(1e-21, 3)
a2.set_xlim(0, 45)
a2.set_yticks([1, 1e-5, 1e-10, 1e-15, 1e-20])
a2.set_yticklabels(["1", "10⁻⁵", "10⁻¹⁰", "10⁻¹⁵", "10⁻²⁰"])
fig.tight_layout()
save(fig, __file__)
