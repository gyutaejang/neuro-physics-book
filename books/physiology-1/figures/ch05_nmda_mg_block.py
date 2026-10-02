from figstyle import plt, np, save, C

# Jahr & Stevens (1990)의 Mg²⁺ 차단 식: B(V) = 1 / (1 + [Mg]/3.57 mM · exp(−0.062 V/mV))
def unblocked(v, mg=1.0):
    return 1 / (1 + mg / 3.57 * np.exp(-0.062 * v))

v = np.linspace(-90, 40, 400)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1.1, 1]))

# 왼쪽: 전류-전압 관계 (역전 전위 0 mV, −80 mV에서 Mg²⁺ 없는 전류를 −1로 둔다)
i_free = v / 80
i_mg = unblocked(v) * v / 80
a1.axhline(0, color=C["gray"], lw=0.6)
a1.axvline(0, color=C["gray"], lw=0.6)
a1.plot(v, i_free, color=C["gray"], lw=1.4, ls="--", label="Mg²⁺ 없음 (또는 AMPA)")
a1.plot(v, i_mg, color=C["blue"], lw=1.8, label="Mg²⁺ 1 mM (NMDA)")
a1.axvspan(-80, -60, color=C["light"], lw=0)
a1.text(-70, 0.38, "휴지\n전위", ha="center", fontsize=8, color=C["ink"])
a1.set_xlabel("막전위 (mV)")
a1.set_ylabel("전류 (상대값, 안쪽 = 음)")
a1.set_xlim(-90, 40)
a1.set_ylim(-1.15, 0.6)
a1.legend(loc="lower right", fontsize=8)
a1.set_title("NMDA 전류는 탈분극해야 커진다", fontsize=10)

# 오른쪽: 막히지 않은 비율
b = unblocked(v) * 100
a2.plot(v, b, color=C["blue"], lw=1.8)
for vv in (-70, -40, -20, 0):
    y = unblocked(vv) * 100
    a2.scatter([vv], [y], color=C["red"], s=20, zorder=4)
    a2.annotate(f"{vv} mV: {y:.0f} %", xy=(vv, y), xytext=(-62, 6) if vv == 0 else (6, -4),
                textcoords="offset points", fontsize=8)
a2.set_xlabel("막전위 (mV)")
a2.set_ylabel("열린 통로 중 막히지 않은 비율 (%)")
a2.set_xlim(-90, 40)
a2.set_ylim(0, 100)
a2.set_title("세포 밖 Mg²⁺ 1 mM", fontsize=10)
fig.tight_layout()
save(fig, __file__)
