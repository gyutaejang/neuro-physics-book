from figstyle import plt, np, save, C

L = np.logspace(-8.5, 0.3, 300)  # m
fig, ax = plt.subplots(figsize=(6.6, 3.1))
for D, lab, col in [(3e-9, "물 (D ≈ 3×10⁻⁹ m²/s)", C["blue"]),
                    (5e-10, "작은 분자, 신경전달물질 (≈ 5×10⁻¹⁰)", C["green"]),
                    (1e-11, "큰 단백질, 세포질 안 (≈ 10⁻¹¹)", C["purple"])]:
    ax.loglog(L, L ** 2 / (2 * D), color=col, lw=1.6, label=lab)
for t, name in [(1e-6, "1 μs"), (1e-3, "1 ms"), (1, "1 s"), (3600, "1시간"), (86400, "1일"),
                (3.15e7, "1년")]:
    ax.axhline(t, color=C["gray"], lw=0.5, ls=":")
    ax.text(2.6, t, name, fontsize=8, va="center", color=C["gray"])
for Lm, name in [(2e-8, "시냅스 틈\n20 nm"), (2.5e-5, "모세혈관 사이\n~25 μm"),
                 (3e-3, "피질 두께\n3 mm "), (1e-2, " 1 cm"), (1, "긴 축삭\n1 m")]:
    ax.axvline(Lm, color=C["red"], lw=0.6, ls="--", alpha=0.7)
    ha = "right" if Lm == 3e-3 else ("left" if Lm == 1e-2 else "center")
    ax.text(Lm, 3e12, name, fontsize=8, ha=ha, va="bottom", color=C["red"])
ax.set_xlim(3e-9, 2.5)
ax.set_ylim(1e-9, 3e12)
ax.set_xticks([1e-8, 1e-6, 1e-4, 1e-2, 1])
ax.set_xticklabels(["10 nm", "1 μm", "100 μm", "1 cm", "1 m"])
ax.set_yticks([1e-9, 1e-6, 1e-3, 1, 1e3, 1e6, 1e9, 1e12])
ax.set_yticklabels(["1 ns", "1 μs", "1 ms", "1 s", "10³ s", "10⁶ s", "10⁹ s", "10¹² s"])
ax.minorticks_off()
ax.set_xlabel("거리 L")
ax.set_ylabel("확산 시간 t ≈ L²/2D")
ax.legend(fontsize=8, loc="upper left")
save(fig, __file__)
