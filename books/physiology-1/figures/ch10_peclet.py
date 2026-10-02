from figstyle import plt, np, save, C

lam = 1.6                     # 굴곡도
L = np.logspace(-6, -2, 300)  # 거리 (m): 1 μm ~ 1 cm
diff = [(1.24e-9, "작은 분자 (TMA⁺, 포도당 수준)", C["green"], "-"),
        (1.5e-10, "아밀로이드 베타 단량체", C["green"], "--"),
        (4e-11, "항체 같은 큰 단백질", C["green"], ":")]
flow = [(0.1e-6, "0.1 μm/s"), (1e-6, "1 μm/s"), (20e-6, "20 μm/s")]

fig, ax = plt.subplots(figsize=(6.8, 3.7))
for D, lab, col, ls in diff:
    Ds = D / lam ** 2
    ax.loglog(L * 1e6, L ** 2 / (2 * Ds), color=col, lw=1.8, ls=ls, label="확산: " + lab)
ax.set_xlim(1, 1e4)
ax.set_ylim(1e-3, 1e7)
fig.canvas.draw()


def angle(slope):
    p0 = ax.transData.transform((10, 1))
    p1 = ax.transData.transform((100, 10 ** slope))
    return np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))


for v, lab in flow:
    ax.loglog(L * 1e6, L / v, color=C["blue"], lw=1.2, alpha=0.9)
    xt = 2.2 if v < 1e-5 else 1500
    ax.text(xt, xt * 1e-6 / v * 1.6, "흐름 " + lab, color=C["blue"], fontsize=8,
            rotation=angle(1), rotation_mode="anchor", ha="left", va="bottom")
for sec, lab in ((1, "1초"), (60, "1분"), (3600, "1시간"), (86400, "1일")):
    ax.axhline(sec, color=C["gray"], lw=0.5, ls=":")
    ax.text(1.05e4, sec, lab, fontsize=8, color=C["gray"], va="center", ha="left")
ax.axvspan(100, 300, color=C["gray"], alpha=0.12, lw=0)
ax.text(173, 1e6, "동맥 주위 → 정맥 주위\n거리 약 100–300 μm", fontsize=8, ha="center", color=C["ink"])
ax.set_xlim(1, 1e4)
ax.set_ylim(1e-3, 1e7)
ax.set_xticks([1, 10, 100, 1000, 10000])
ax.set_xticklabels(["1 μm", "10 μm", "100 μm", "1 mm", "1 cm"])
ax.set_yticks([1e-2, 1, 1e2, 1e4, 1e6])
ax.set_yticklabels(["10⁻²", "1", "10²", "10⁴", "10⁶"])
ax.minorticks_off()
ax.set_xlabel("옮겨야 할 거리")
ax.set_ylabel("걸리는 시간 (s)")
ax.legend(fontsize=7.5, loc="upper left")
fig.tight_layout()
save(fig, __file__)
