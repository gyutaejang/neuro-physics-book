from figstyle import plt, np, C, save

# 질량 감쇠 계수 μ/ρ (cm²/g), NIST XCOM 표의 근삿값.
E_T = np.array([15, 20, 30, 40, 50, 60, 80, 100, 150.])
WATER = np.array([1.673, 0.8096, 0.3756, 0.2683, 0.2269, 0.2059, 0.1837, 0.1707, 0.1505])
BONE = np.array([9.032, 4.001, 1.331, 0.6655, 0.4242, 0.3148, 0.2229, 0.1855, 0.1480])  # 피질골, 1.92 g/cm³
# 요오드: K 흡수 끝(33.2 keV)에서 불연속
I_LO_E = np.array([15, 20, 30, 33.17]); I_LO = np.array([55.0, 25.9, 8.6, 6.55])
I_HI_E = np.array([33.17, 40, 50, 60, 80, 100, 150]); I_HI = np.array([36.3, 22.1, 12.3, 7.58, 3.51, 1.94, 0.70])


def li(E, et, tab):
    return np.exp(np.interp(np.log(E), np.log(et), np.log(tab)))


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw=dict(width_ratios=[1, 1.1]))
ax = axes[0]
E = np.geomspace(15, 150, 300)
ax.loglog(E, li(E, E_T, WATER), color=C["blue"], lw=1.8)
ax.loglog(E, li(E, E_T, BONE), color=C["ink"], lw=1.8)
e1 = np.geomspace(15, 33.17, 80); e2 = np.geomspace(33.17, 150, 150)
ax.loglog(np.r_[e1, e2], np.r_[li(e1, I_LO_E, I_LO), li(e2, I_HI_E, I_HI)], color=C["red"], lw=1.8)
ax.text(110, 0.205, "물 (연조직)", color=C["blue"], fontsize=9, ha="center", va="bottom")
ax.text(40, 0.8, "뼈", color=C["ink"], fontsize=9)
ax.text(85, 5.0, "요오드", color=C["red"], fontsize=9)
ax.annotate("K 흡수 끝\n33.2 keV", xy=(33.5, 20), xytext=(16, 3.0), fontsize=8.5, color=C["red"],
            arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.7))
ax.axvspan(50, 70, color=C["light"], zorder=0)
ax.text(59, 40, "CT 평균\n에너지", fontsize=8, ha="center", color=C["gray"])
ax.set_xlim(15, 150); ax.set_ylim(0.1, 80)
ax.set_xticks([20, 30, 50, 100, 150]); ax.set_xticklabels(["20", "30", "50", "100", "150"])
ax.minorticks_off()
ax.set_yticks([0.1, 1, 10]); ax.set_yticklabels(["0.1", "1", "10"])
ax.set_xlabel("광자 에너지 (keV)")
ax.set_ylabel("질량 감쇠 계수 μ/ρ (cm²/g)")
ax.set_title("(가) 물질과 에너지에 따른 감쇠", fontsize=10.5)

# (나) 머리를 가로지르는 한 줄: 두피 0.5, 뼈 0.7, 뇌 16, 뼈 0.7, 두피 0.5 cm
ax = axes[1]
layers = [(0.5, "soft"), (0.7, "bone"), (16.0, "soft"), (0.7, "bone"), (0.5, "soft")]
edges = np.cumsum([0] + [d for d, _ in layers])
for (d, kind), x0 in zip(layers, edges[:-1]):
    if kind == "bone":
        ax.axvspan(x0, x0 + d, color=C["gray"], alpha=0.25, lw=0)
for Ek, col, ls in [(40, C["red"], "--"), (70, C["blue"], "-")]:
    mus = {"soft": li(Ek, E_T, WATER) * 1.0, "bone": li(Ek, E_T, BONE) * 1.92}
    x = np.linspace(0, edges[-1], 800)
    mu = np.zeros_like(x)
    for (d, kind), x0 in zip(layers, edges[:-1]):
        mu[(x >= x0) & (x <= x0 + d)] = mus[kind]
    T = np.exp(-np.concatenate([[0], np.cumsum(mu[1:] * np.diff(x))]))
    ax.semilogy(x, T, color=col, lw=1.8, ls=ls)
    print(Ek, "keV 투과율", T[-1])
    ax.text(edges[-1] + 0.3, T[-1], f"{Ek} keV\n{T[-1] * 100:.1f}%", color=col, fontsize=8.5, va="center")
ax.text(edges[1] + 0.35, 1.7, "뼈", fontsize=8.5, color=C["gray"], ha="center")
ax.text(edges[4] - 0.35, 1.7, "뼈", fontsize=8.5, color=C["gray"], ha="center")
ax.text(9.5, 0.4, "뇌 (물과 비슷)", fontsize=9, ha="center", color=C["ink"])
ax.set_xlim(0, edges[-1] + 3.5)
ax.set_ylim(5e-4, 3)
ax.set_xticks([0, 5, 10, 15, 18.4]); ax.set_xticklabels(["0", "5", "10", "15", "18.4"])
ax.set_xlabel("머리 속 깊이 (cm)")
ax.set_ylabel("남은 세기 I/I₀")
ax.set_title("(나) 머리를 지나는 X선 한 줄", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
