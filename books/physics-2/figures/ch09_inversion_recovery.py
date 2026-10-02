from figstyle import plt, np, save, C

# 반전 회복: 180° 뒤 Mz(TI) = M0 (1 − 2 e^{−TI/T1})  (TR이 T1보다 충분히 길다고 둔다).
tis = {
    "지방": (380, C["purple"], ":"),
    "백질": (850, C["blue"], "-"),
    "회백질": (1400, C["red"], "-"),
    "뇌척수액": (4000, C["green"], "--"),
}
TI = np.linspace(0, 6000, 1200)
fig, ax = plt.subplots(figsize=(6.8, 3.4))
ax.axhline(0, color=C["gray"], lw=0.8)
for name, (T1, col, ls) in tis.items():
    ax.plot(TI, 1 - 2 * np.exp(-TI / T1), color=col, ls=ls, lw=1.6, label=f"{name} (T1 {T1} ms)")
    tn = T1 * np.log(2)
    ax.plot([tn], [0], "o", color=col, ms=5, zorder=5)
tn_csf = 4000 * np.log(2)
ax.annotate(f"뇌척수액 무효화 (FLAIR)\nTI = T1·ln2 ≈ {tn_csf:.0f} ms", xy=(tn_csf, 0), xytext=(2400, -0.5),
            fontsize=8.5, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.annotate(f"지방 무효화 ≈ {380 * np.log(2):.0f} ms (STIR)", xy=(380 * np.log(2), 0), xytext=(450, 1.13),
            fontsize=8.5, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.annotate(f"백질 {850 * np.log(2):.0f} ms", xy=(850 * np.log(2), 0), xytext=(1050, -0.3),
            fontsize=8, color=C["blue"], arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.annotate(f"회백질 {1400 * np.log(2):.0f} ms", xy=(1400 * np.log(2), 0), xytext=(1800, 0.02),
            fontsize=8, color=C["red"], arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.set_xlim(0, 6000)
ax.set_ylim(-1.05, 1.3)
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_xlabel("반전 시간 TI (ms)")
ax.set_ylabel("$M_z$ / $M_0$")
ax.legend(fontsize=8, loc="lower right")
save(fig, __file__)
