from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.2))

# (가) 18 cm 물 경로 위 선원 위치에 따른 생존 확률
Lh = 18.0
z = np.linspace(0, Lh, 200)
mu511, mu140 = 0.096, 0.15  # 물의 선형 감쇠 계수 (1/cm)
pet = np.exp(-mu511 * Lh) * np.ones_like(z)
a1.plot(z, pet, color=C["blue"], lw=2, label="PET 광자 쌍 (511 keV)")
a1.plot(z, np.exp(-mu511 * z), color=C["blue"], lw=1, ls=":", label="511 keV 광자 하나 (왼쪽 검출기로)")
a1.plot(z, np.exp(-mu140 * z), color=C["red"], lw=1.6, ls="--", label="SPECT 광자 (140 keV, 왼쪽 검출기로)")
a1.text(5, pet[0] - 0.03, f"선원이 어디 있든 {pet[0] * 100:.0f}%", ha="center", va="top", fontsize=8, color=C["blue"])
a1.set_xlim(0, Lh)
a1.set_ylim(0, 1.05)
a1.set_xlabel("왼쪽 표면에서 선원까지의 깊이 (cm)")
a1.set_ylabel("감쇠되지 않고 나올 확률")
a1.legend(fontsize=7.4, loc="upper right")
a1.set_title("(가) 지름 18 cm 물 머리의 감쇠", fontsize=9.5)

# (나) 콤프턴 산란 뒤 광자 에너지
th = np.linspace(0, 180, 400)
E = 511 / (2 - np.cos(np.radians(th)))
a2.axhspan(425, 650, color=C["light"], zorder=0)
a2.text(178, 600, "에너지 창 425–650 keV", ha="right", fontsize=8, color=C["gray"])
a2.plot(th, E, color=C["blue"], lw=1.8)
t425 = np.degrees(np.arccos(2 - 511 / 425))
a2.axvline(t425, color=C["red"], lw=0.8, ls="--")
a2.annotate(f"{t425:.0f}° 이하로 꺾인 광자는\n창 안에 남는다", xy=(t425, 425), xytext=(55, 470), fontsize=8,
            color=C["red"], arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
for a, dx, dy, ha in ((30, -4, -20, "right"), (90, 4, 8, "left"), (180, -3, 22, "right")):
    e = 511 / (2 - np.cos(np.radians(a)))
    a2.scatter([a], [e], color=C["ink"], s=14, zorder=3)
    a2.text(a + dx, e + dy, f"{a}°: {e:.0f} keV", fontsize=7.6, va="center", ha=ha)
a2.set_xlim(0, 182)
a2.set_ylim(130, 680)
a2.set_xticks([0, 30, 60, 90, 120, 150, 180])
a2.set_xlabel("산란각 (°)")
a2.set_ylabel("산란된 광자 에너지 (keV)")
a2.set_title("(나) 511 keV 광자의 콤프턴 산란", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
