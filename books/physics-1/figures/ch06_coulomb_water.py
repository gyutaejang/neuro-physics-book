from figstyle import plt, np, save, C

# Na+ 와 Cl- 사이의 전기적 위치에너지 크기 |U| = k e^2 / (eps_r r), kT 단위로
k, e = 8.99e9, 1.602e-19
kT = 1.381e-23 * 310
r = np.linspace(0.25, 3.0, 300)  # nm
U_vac = k * e * e / (r * 1e-9) / kT
U_wat = U_vac / 80

fig, ax = plt.subplots(figsize=(6.4, 3.1))
ax.semilogy(r, U_vac, color=C["blue"], label="진공 (εᵣ = 1)")
ax.semilogy(r, U_wat, color=C["green"], label="물 (εᵣ ≈ 80)")
ax.axhline(1, color=C["red"], lw=1, ls="--")
ax.text(2.95, 1.25, "열에너지 kT (37 °C)", color=C["red"], fontsize=8.5, ha="right", va="bottom")
ax.annotate("", xy=(0.5, U_wat[np.argmin(abs(r - 0.5))]), xytext=(0.5, U_vac[np.argmin(abs(r - 0.5))]),
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=1))
ax.text(0.56, 12, "물속에서\n80분의 1", fontsize=8.5, color=C["gray"], va="center")
ax.scatter([0.5, 0.5], [107.8, 1.35], color=[C["blue"], C["green"]], s=18, zorder=4)
ax.text(1.0, 108, "0.5 nm에서 약 110 kT", fontsize=8.5, color=C["blue"])
ax.text(1.0, 2.2, "0.5 nm에서 약 1.3 kT", fontsize=8.5, color=C["green"])
ax.set_xlabel("이온 사이 거리 r (nm)")
ax.set_ylabel("끌어당김 에너지 (kT 단위)")
ax.set_xlim(0.25, 3.0)
ax.set_ylim(0.1, 400)
ax.legend(loc="upper right", fontsize=8.5)
save(fig, __file__)
