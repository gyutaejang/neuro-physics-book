from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1.1, 1]))

# 왼쪽: 물 분자 두 개 사이의 수소 결합 (길이는 nm, 실제 비율)
def atom(ax, x, y, el):
    r = 0.028 if el == "O" else 0.018
    fc = C["blue"] if el == "O" else "white"
    ax.add_patch(plt.Circle((x, y), r, facecolor=fc, edgecolor=C["ink"], lw=0.8, alpha=0.85 if el == "O" else 1, zorder=3))
    ax.text(x, y, el, ha="center", va="center", fontsize=8, color="white" if el == "O" else C["ink"], zorder=4)

d, ang = 0.096, np.deg2rad(104.5)
O1 = np.array([0.0, 0.0])
H1 = O1 + d * np.array([1, 0])
H2 = O1 + d * np.array([np.cos(ang), np.sin(ang)])
O2 = np.array([0.282, 0.0])
H3 = O2 + d * np.array([np.cos(np.deg2rad(52)), np.sin(np.deg2rad(52))])
H4 = O2 + d * np.array([np.cos(np.deg2rad(52)), -np.sin(np.deg2rad(52))])
for a, b in ((O1, H1), (O1, H2), (O2, H3), (O2, H4)):
    a1.plot([a[0], b[0]], [a[1], b[1]], color=C["ink"], lw=2, zorder=2)
a1.plot([H1[0], O2[0]], [0, 0], color=C["red"], lw=1.6, ls=(0, (2, 2)), zorder=2)
for p, el in ((O1, "O"), (H1, "H"), (H2, "H"), (O2, "O"), (H3, "H"), (H4, "H")):
    atom(a1, *p, el)
a1.text(O1[0] - 0.04, -0.03, "δ−", fontsize=9, ha="right", va="top", color=C["blue"])
a1.text(H1[0] + 0.005, 0.03, "δ+", fontsize=9, ha="center", color=C["red"])
a1.text(O2[0] - 0.01, -0.045, "δ−", fontsize=9, ha="center", va="top", color=C["blue"])
a1.text((H1[0] + O2[0]) / 2 + 0.005, 0.022, "수소 결합\n약 0.18 nm", fontsize=8.5, ha="center", va="bottom", color=C["red"])
a1.text(0.048, -0.035, "공유 결합\n0.10 nm", fontsize=8, ha="center", va="top", color=C["ink"])
a1.annotate("", xy=(O1[0], -0.135), xytext=(O2[0], -0.135),
            arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=1))
a1.text(O2[0] / 2, -0.145, "O···O 약 0.28 nm", fontsize=8.5, ha="center", va="top", color=C["gray"])
a1.text(-0.02, 0.125, "주개 (H를 내줌)", fontsize=8.5, ha="center", color=C["ink"])
a1.text(O2[0] + 0.03, 0.125, "받개 (비공유 전자쌍)", fontsize=8.5, ha="center", color=C["ink"])
a1.text(0.04, 0.032, "104.5°", fontsize=7.5, color=C["gray"], ha="center")
a1.set_xlim(-0.12, 0.42)
a1.set_ylim(-0.2, 0.16)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 물과 얼음의 밀도 (Kell 1975 식)
T = np.linspace(0, 100, 400)
rho = (999.83952 + 16.945176 * T - 7.9870401e-3 * T**2 - 46.170461e-6 * T**3
       + 105.56302e-9 * T**4 - 280.54253e-12 * T**5) / (1 + 16.879850e-3 * T) / 1000
Ti = np.linspace(-20, 0, 50)
rho_ice = 0.9167 + (0.9195 - 0.9167) * (-Ti / 20)
a2.plot(T, rho, color=C["blue"], lw=1.8)
a2.plot(Ti, rho_ice, color=C["purple"], lw=1.8)
a2.plot([0, 0], [0.9167, 0.99984], color=C["gray"], lw=0.8, ls=":")
a2.text(-10, 0.925, "얼음\n0.917", color=C["purple"], fontsize=8.5, ha="center", va="bottom")
a2.text(55, 0.993, "액체 물", color=C["blue"], fontsize=8.5, ha="left")
a2.annotate("4 °C에서 최대\n1.000 g/cm³", xy=(4, 0.99997), xytext=(20, 0.945), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
a2.scatter([37], [0.99333], color=C["green"], s=20, zorder=4)
a2.annotate("37 °C: 0.993", xy=(37, 0.99333), xytext=(45, 1.004), fontsize=8.5, color=C["green"],
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
a2.text(3, 0.93, "얼음이 녹으면\n밀도가 약 9% 커진다", fontsize=8, color=C["gray"], ha="left", va="center")
a2.set_xlim(-22, 102)
a2.set_ylim(0.905, 1.012)
a2.set_xlabel("온도 (°C)")
a2.set_ylabel("밀도 (g/cm³)")
a2.set_xticks([-20, 0, 20, 40, 60, 80, 100])
a2.set_xticklabels(["−20", "0", "20", "40", "60", "80", "100"])
fig.tight_layout()
save(fig, __file__)
